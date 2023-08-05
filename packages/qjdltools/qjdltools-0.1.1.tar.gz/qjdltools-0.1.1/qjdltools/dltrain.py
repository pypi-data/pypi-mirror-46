'''
Tools collection of operations during training.
The icluded functions are:
    def train_log()
    def draw_loss_curve()
    def memory_watcher()
    def Accuracy Evaluation[serval functions]

Version 1.0  2018-04-02 22:44:32
    by QiJi Refence: https://github.com/GeorgeSeif/Semantic-Segmentation-Suite
Version 2.0  2018-10-29 09:10:41
    by QiJi
TODO:


'''
import datetime
import os
import sys

import numpy as np
from skimage import morphology
# from sklearn import metrics
from matplotlib import pyplot as plt


def train_log(X, f=None):
    ''' Print with time. To console or a file(f) '''
    time_stamp = datetime.datetime.now().strftime("[%d %H:%M:%S]")
    if not f:
        sys.stdout.write(time_stamp + " " + X)
        sys.stdout.flush()
    else:
        f.write(time_stamp + " " + X)


def draw_loss_curve(epochs, loss, path):
    ''' Paint loss curve '''
    fig = plt.figure(figsize=(12, 9))
    ax1 = fig.add_subplot(111)
    ax1.plot(range(epochs), loss)
    ax1.set_title("Average loss vs epochs")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Current loss")
    plt.savefig(path + '/loss_vs_epochs.png')
    plt.close(fig)


def memory_watcher():
    ''' Compute the memory usage, for debugging '''
    import psutil
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0] / 2.**30  # Memory use in GB
    print('Memory usage in GBs:', memoryUse)


# **********************************************
# *********** Segmention Evaluation **************
# **********************************************
def fast_hist(label_true, label_pred, n_class):
    '''Computational confusion matrix.
    -------------------------------------------
    |          | p_cls_1 | p_cls_2 |   ....   |
    -------------------------------------------
    | gt_cls_1 |         |         |          |
    -------------------------------------------
    | gt_cls_2 |         |         |          |
    -------------------------------------------
    |   ....   |         |         |          |
    -------------------------------------------
    '''
    # mask = (label_true >= 0) & (label_true < n_class)
    if len(label_true.shape) > 1:
        label_true = label_true.flatten()
        label_pred = label_pred.flatten()
    hist = np.bincount(
        n_class * label_true.astype(int) + label_pred,
        minlength=n_class ** 2,
    ).reshape(n_class, n_class)
    return hist


def compute_global_accuracy(pred, label):
    '''
    Compute the average segmentation accuracy across all classes,
    Input [HW] or [HWC] label
    '''
    count_mat = pred == label
    return np.sum(count_mat) / np.prod(count_mat.shape)


def compute_class_accuracies(y_pred, y_true, num_classes):
    ''' Compute the class-specific segmentation accuracy '''
    w = y_true.shape[0]
    h = y_true.shape[1]
    flat_image = np.reshape(y_true, w * h)
    total = []
    for val in range(num_classes):
        total.append((flat_image == val).sum())

    count = [0.0] * num_classes
    for i in range(w):
        for j in range(h):
            if y_pred[i, j] == y_true[i, j]:
                count[int(y_pred[i, j])] = count[int(y_pred[i, j])] + 1.0
    # If there are no pixels from a certain class in the GT, it returns NAN
    # because of divide by zero, Replace the nans with a 1.0.
    accuracies = []
    for i in range(len(total)):
        if total[i] == 0:
            accuracies.append(1.0)
        else:
            accuracies.append(count[i] / total[i])

    return accuracies


def compute_class_iou(pred, gt, num_classes):
    '''
    Args:
        pred: Predict label [HW].
        gt: Ground truth label [HW].
    Return:
        （每一类的）intersection and union list.
    '''
    intersection = np.zeros(num_classes)
    union = np.zeros(num_classes)
    for i in range(num_classes):
        pred_i = pred == i
        label_i = gt == i
        intersection[i] = float(np.sum(np.logical_and(label_i, pred_i)))
        union[i] = float(np.sum(np.logical_or(label_i, pred_i)) + 1e-8)
    class_iou = intersection / union
    return class_iou


class runingScore(object):
    ''' Evaluation class '''
    def __init__(self, n_classes=2):
        self.n_classes = n_classes
        self.confusion_matrix = np.zeros((n_classes, n_classes), dtype=np.int64)

    def reset(self):
        ''' Reset confusion_matrix. '''
        self.confusion_matrix = np.zeros((self.n_classes, self.n_classes), dtype=np.int64)

    def update_all(self, label_trues, label_preds):
        ''' Add new pairs of predicted label and GT label to update the confusion_matrix.
        Note: Only suitable for segmentation
        '''
        for lt, lp in zip(label_trues, label_preds):
            self.confusion_matrix += fast_hist(lt, lp, self.n_classes)

    def print_score(self, score, mode=0):
        ''' Print the score dict.
        mode-0: print the final total scores
        mode-1: print per pair of data's scores
        '''
        str_score = ''
        for key in score:
            if 'Class' in key:
                value_str = ','.join('%.4f' % i for i in score[key])
            elif 'Hist' in key:
                continue
            else:
                value_str = '%.4f' % score[key]
            str_score += '%s,' % value_str if mode else key+': %s\n' % value_str
        str_score = str_score.strip(',').strip()  # discard the last suffix
        if mode == 0:
            print(str_score)

        return str_score


class classifyScore(runingScore):
    ''' Accuracy evaluation for classification(multi-class)'''
    def update(self, label_true, label_pred):
        '''Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix.'''
        hist = fast_hist(label_true, label_pred, self.n_classes)
        self.confusion_matrix += hist
        # return self.get_scores(hist)

    def get_scores(self, hist=None):
        """Returns accuracy score evaluation result.
            - Overall Acc
            - Class Acc
            - Mean Acc
        """
        hist = self.confusion_matrix if hist is None else hist
        # Overall accuracy
        acc_overall = np.diag(hist).sum() / (hist.sum()+1e-8)
        # Class accuracy
        acc_cls = np.diag(hist) / (hist.sum(axis=1)+1e-8)  # acc per class
        # Class average accuracy
        acc_cls_avg = np.nanmean(acc_cls)
        # Kappa
        n = hist.sum()
        p0 = hist.diagonal().sum()
        p1 = hist.sum(0)
        p2 = hist.sum(1)
        kappa = (n*p0-np.inner(p1, p2)) / (n*n - np.inner(p1, p2) + 1e-8)

        return (
            {
                "Hist": hist,  # 混淆矩阵
                "Kappa": kappa,
                "Overall Acc": acc_overall,
                "Class Acc": acc_cls,  # 类别精度
                "Mean Acc": acc_cls_avg,
            }  # Return as a dictionary
        )


class SegScore(runingScore):
    ''' Accuracy evaluation for semantic segmentation(multi-class)'''
    def update(self, label_true, label_pred):
        '''Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix.'''
        hist = fast_hist(label_true, label_pred, self.n_classes)
        self.confusion_matrix += hist
        return self.get_scores(hist)

    def get_scores(self, hist=None):
        """Use the confusion_matrix to do evaluation.
        Returns accuracy score evaluation result:
            - Overall Acc
            - Class Acc
            - Mean Acc
            - Class IoU
            - Mean IoU
            - FreqW Acc
        """
        hist = self.confusion_matrix if hist is None else hist
        # Overall accuracy
        acc_overall = np.diag(hist).sum() / hist.sum()
        # Class accuracy
        acc_cls = np.diag(hist) / hist.sum(axis=1)  # acc per class
        # Class average accuracy
        acc_cls_avg = np.nanmean(acc_cls)

        # IoU
        ep = np.ones((hist.shape[0])) * 1e-8
        cls_iu = np.diag(hist) / (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist) + ep)
        mean_iu = np.nanmean(cls_iu)
        # Frequency Weighted IoU(FWIoU) 根据每个类出现的频率为其设置权重
        freq = hist.sum(axis=1) / hist.sum()
        fwavacc = (freq[freq > 0] * cls_iu[freq > 0]).sum()
        # cls_iu = dict(zip(range(self.n_classes), iu))

        return (
            {
                "Overall Acc": acc_overall,
                "Class Acc": acc_cls,  # 类别精度
                "Mean Acc": acc_cls_avg,
                "Class IoU": cls_iu,
                "Mean IoU": mean_iu,
                "FreqW Acc": fwavacc,
            }  # Return as a dictionary
        )


class RoadExtractionScore(runingScore):
    '''Accuracy evaluation for road extraction.
    Only two class: 0-bg, 1-road.
    '''

    def update(self, label_true, label_pred):
        '''Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix. '''
        hist = fast_hist(label_true, label_pred, self.n_classes)
        self.confusion_matrix += hist
        return self.get_scores(hist)

    def add(self, label_true, label_pred):
        '''Add a new pair of predicted label and GT label,
        update the confusion_matrix. '''
        hist = fast_hist(label_true, label_pred, self.n_classes)
        self.confusion_matrix += hist

    def get_scores(self, hist=None):
        """Returns accuracy score evaluation result.
            - 1. Precision{ TP / (TP+FP) }
            - 2. Recall{ TP / (TP+FN) }
            - 3. F1score
            - 4. Class IoU
            - 5. Mean IoU
            - 6. FreqW Acc
        """
        hist = self.confusion_matrix if hist is None else hist

        # Take class 1-road as postive class:
        TP = hist[1, 1]  # Ture Positive(road pixels are classified into road class)
        FN = hist[1, 0]  # False Negative(road pixels are classified into bg class)
        FP = hist[0, 1]  # False Positive(bg pixels are classified into road class)
        # TN = hist[0, 0]  # Ture Negative(bg pixels are classified into bg class)

        prec = TP / (TP + FP + 1e-8)  # Precision
        rec = TP / (TP + FN + 1e-8)  # Recall
        F1 = 2*TP / (2*TP + FP + FN + 1e-8)  # F1 Score

        # IoU (tested)
        cls_iu = np.diag(hist) / (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist))
        mean_iu = np.nanmean(cls_iu)
        # Frequency Weighted IoU(FWIoU) 根据每个类出现的频率为其设置权重
        freq = hist.sum(axis=1) / hist.sum()
        fwavacc = (freq[freq > 0] * cls_iu[freq > 0]).sum()
        # cls_iu = dict(zip(range(self.n_classes), iu))

        return (
            {
                'Precision': prec,
                'Recall': rec,
                'F1score': F1,
                'Class IoU': cls_iu,
                'Mean IoU': mean_iu,
                'FreqW Acc': fwavacc,
            }  # Return as a dictionary
        )

    def keys(self):
        score_keys = [
            'Precision,Recall,F1score,Class IoU,Class IoU,Mean IoU,FreqW Acc'
            ]  # note 'Class IoU'
        return score_keys


class RelaxedRoadExtractionScore(runingScore):
    '''Relax Accuracy evaluation for road extraction.
    Only two class: 0-bg, 1-road.
    '''
    def __init__(self, rho=1):
        self.rho = rho*2 + 1
        self.confusion_matrix_p = np.zeros((2, 2), np.int64)  # For relaxed precision
        self.confusion_matrix_r = np.zeros((2, 2), np.int64)  # For relaxed recall

    def update(self, label_true, label_pred):
        '''Evaluate a new pair of predicted label and GT label,
        and update the confusion_matrix.'''
        if self.rho > 1:
            selem = morphology.square(self.rho, dtype=label_true.dtype)
            tp_label_true = morphology.dilation(label_true, selem)
            tp_label_pred = morphology.binary_dilation(label_pred, selem)
            hist1 = fast_hist(tp_label_true, label_pred, 2)
            hist2 = fast_hist(label_true, tp_label_pred, 2)
        else:
            hist = fast_hist(label_true, label_pred, 2)
            hist1, hist2 = hist, hist

        self.confusion_matrix_p += hist1
        self.confusion_matrix_r += hist2
        return self.get_scores(hist1, hist2)

    def add(self, label_true, label_pred):
        ''' Add new pairs of predicted label and GT label to update the confusion_matrix. '''
        if self.rho > 0:
            selem = morphology.square(self.rho, dtype=np.int64)
            tp_lt = morphology.binary_dilation(label_true, selem)
            tp_lp = morphology.binary_dilation(label_pred, selem)
            self.confusion_matrix_p += fast_hist(tp_lt, label_pred, 2)
            self.confusion_matrix_r += fast_hist(label_true, tp_lp, 2)
        else:
            hist = fast_hist(label_true, label_pred, 2)
            self.confusion_matrix_p += hist
            self.confusion_matrix_r += hist

    def get_scores(self, hist_p=None, hist_r=None):
        hist_p = self.confusion_matrix_p if hist_p is None else hist_p
        hist_r = self.confusion_matrix_r if hist_r is None else hist_r

        prec = hist_p[1, 1] / (hist_p[1, 1] + hist_p[0, 1] + 1e-8)  # Precision
        rec = hist_r[1, 1] / (hist_r[1, 1] + hist_r[1, 0] + 1e-8)  # Recall
        return (
            {
                "Precision": prec,
                "Recall": rec,
                # "F1score":
            }  # Return as a dictionary
        )

    def reset(self):
        ''' Reset confusion_matrixs. '''
        self.confusion_matrix_p = np.zeros((2, 2), dtype=np.int64)
        self.confusion_matrix_r = np.zeros((2, 2), dtype=np.int64)


# **********************************************
# ***********                     **************
# **********************************************
def test():
    # Test confusion_matrix
    # n_class = 2
    pre = np.zeros((10, 10), dtype=np.int32)
    gt = np.zeros((10, 10), dtype=np.int32)
    # # 0-BG; 1-Road
    pre[4:6, 4:6] = 1
    gt[4:6, 4:6] = 1  # 4 road piexls
    # print(gt)
    # print(pre)
    pre[4, 4] = 0  # 有1个原本是road 的被分为0-bg
    # pre[1:8, 1] = 1  # 有8个原本是bg 的被分为1-road
    # print(len(p.shape))
    # myscore = RelaxedRoadExtractionScore(rho=3)
    myscore = classifyScore(5)
    myscore.update(gt, pre)
    score = myscore.get_scores()
    myscore.print_score(score)
    # print('FP = ', hist[0, 1])
    # print('FN = ', hist[1, 0])
    # print('P = ', hist[1, 1] / (hist[1, 1]+hist[0, 1]))
    # print('R = ', hist[1, 1] / (hist[1, 1]+hist[1, 0]))
    # test = np.diag(hist)
    # print(test)


if __name__ == "__main__":
    test()
    pass
