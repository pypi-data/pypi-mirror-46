import numpy as np
import scipy.stats as stats


def compere_classifiers(measure_list, names_list, base_classifier=None, level=0.05):
    """
    Compute the statistic significance of the classifiers and prints the results to the stdout
    Procedure is described in an article - Statistical Comparisons of Classifiers over Multiple Data Sets
    Reference:
        @article{demvsar2006statistical,
          title={Statistical comparisons of classifiers over multiple data sets},
          author={Dem{\v{s}}ar, Janez},
          journal={Journal of Machine learning research},
          volume={7},
          number={Jan},
          pages={1--30},
          year={2006}
        }

    :param measure_list: np.array of the measures of the classifiers for each dataset
    :param names_list: list of names of the classifiers (with the same length as measure_list.shape[1])
    :return: boolean matrix ([i, j] is true iff the i-th classifier is significantly better than j-th)
    """
    out = np.zeros((len(names_list), len(names_list)), dtype=np.bool)
    if len(measure_list[0]) == 2:
        print("detected 2 classifiers - applying Wilcoxon signed-ranks test")
        d = measure_list[:, 0] - measure_list[:, 1]
        r = stats.rankdata(d)
        rplus = np.sum(r[d > 0]) + 0.5 * np.sum(r[d == 0])
        rminus = np.sum(r[d < 0]) + 0.5 * np.sum(r[d == 0])
        if len(measure_list) > 25:
            t, p = stats.wilcoxon(measure_list[:, 0], measure_list[:, 1])
            reject = p < level
        else:
            print("Low number of observations, please insert the critical value for your test.")
            print("Wilcoxon Signed-Rank Test with n = {} and alpha = {} "
                  "(see https://math.ucalgary.ca/files/math/wilcoxon_signed_rank_table.pdf for result)"
                  .format(len(measure_list), level))
            cv = float(input("Input value: "))
            t = min(rplus, rminus)
            reject = t < cv
        if reject:
            if rplus > rminus:
                print("The classifier {} (0) is significantly better than the classifier {} (1)."
                      .format(names_list[0], names_list[1]))
                out[0, 1] = True
            else:
                print("The classifier {} (1) is significantly better than the classifier {} (2)."
                      .format(names_list[1], names_list[0]))
                out[1, 0] = True
        else:
            print("The difference between classifiers is not significant, i.e., probably random.")
    else:
        print("detected {} classifiers - applying Friedman test modified to less conservative F-distributed "
              "with Hommel procedure as the post-hoc test")
        k = len(measure_list[0])
        N = len(measure_list)
        mean_r = np.zeros_like(measure_list)
        for i, m in enumerate(measure_list):
            mean_r[i, :] = stats.rankdata(m)
        mean_r = np.mean(mean_r, axis=0)
        diff_r = np.zeros((k, k))
        chif = np.sum((mean_r - (k+1)/2)**2) * 12 * N / k / (k + 1)
        if k > 5 or N > 10:
            f = (N-1) * chif / (N * (k - 1) - chif)
            p = stats.f.cdf(f, k-1, (k-1) * (N-1))
            reject = (1 - p) < level
        else:
            print("Low number of observations or classifiers, please insert the critical value for your test.")
            print("Friedman Test with k = {}, b = {} , alpha = {}"
                  "(see https://www.york.ac.uk/depts/maths/tables/friedman.pdf for result)"
                  .format(k, N, level))
            cv = float(input("Input value: "))
            reject = chif > cv

        if reject:
            print("The difference between classifiers is significant, continuing with post-hoc tests.")
        else:
            print("The difference between classifiers is not significant, i.e., probably random.")
            return out

        for i in range(k):
            for j in range(k):
                diff_r[i, j] = mean_r[i] - mean_r[j]
        z = diff_r / np.sqrt(k * (k + 1) / 6 / N)
        if base_classifier is None:
            print("Compering all classifiers again each other (Nemenyi test).")
            print("Please insert the value for Studentized Range Distribution "
                  "with k = {} and v = infinyty  for alpha = {} \n"
                  "(see https://www.stata.com/stb/stb46/dm64/sturng.pdf for result)"
                  .format(k, level))
            cv = float(input("Input value: "))
            for i in range(k):
                for j in range(k):
                    if z[i, j] > cv / np.sqrt(2):
                        print("The classifier {} ({}) is significantly better than the classifier {} ({})."
                              .format(names_list[i], i, names_list[j], j))
                        out[i, j] = True
        else:
            print("Compering classifier {} ({}) with the others (Holm step down method)."
                  .format(names_list[base_classifier], base_classifier))
            z = z[base_classifier]
            p = np.zeros_like(z)
            for i in range(k):
                if i == base_classifier:
                    p[i] = -np.inf
                else:
                    p[i] = stats.norm.cdf(-np.abs(z[i]))
            sort_index = np.argsort(p)
            sort_index = sort_index[1:]
            for i in range(k-1):
                if p[sort_index[i]] < level / (k - 1):
                    if z[sort_index[i]] > 0:
                        print("The base classifier {} ({}) is significantly better than the classifier {} ({})."
                              .format(names_list[base_classifier], base_classifier,
                                      names_list[sort_index[i]], sort_index[i]))
                        out[base_classifier, sort_index[i]] = True
                    else:
                        print("The base classifier {} ({}) is significantly worst than the classifier {} ({})."
                              .format(names_list[base_classifier], base_classifier,
                                      names_list[sort_index[i]], sort_index[i]))
                        out[sort_index[i], base_classifier] = True
                else:
                    break
    return out

