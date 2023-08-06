# import matplotlib
# # matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import numpy as np
# import seaborn as sns
# import colours

plt.style.use('ggplot')

class Results:
    """Results"""
    def __init__(self):

        self.trial_N = None
        self.results_folder = None
        self.gene_names = None

        self.epochs = 0

        # saves additional data that is defined in the evaluation function
        self.data = {"history": [],
                     "fitness": [],
                     "genes": [],
                     "diversity": [],
                     "average_diversity": []}
        # All are lists of lists. The inner list will contain the values, and the outer list will represent each epoch
        # history: the individuals at each epoch
        # genes: a dictionary with each gene as a key. The corresponding values are that of the genes at each epoch
        # fitness: the fitness scores of each individual at each epoch

    def gene_mins(self, gene):
        return [min(g[gene]) for g in self.data["genes"]]

    def gene_maxs(self, gene):
        return [max(g[gene]) for g in self.data["genes"]]

    def gene_median(self, gene):
        return [np.median(g[gene]) for g in self.data["genes"]]

    def gene_global_min(self, gene):
        return min(self.gene_mins(gene))

    def gene_global_max(self, gene):
        return max(self.gene_maxs(gene))

    def fitness_maxs(self):
        '''returns the maximum fitness in each generation'''
        return [max(f) for f in self.data["fitness"]]

    def fitness_mins(self):
        '''returns the minimum fitness in each generation'''
        return [min(f) for f in self.data["fitness"]]

    def fitness_global_min(self):
        return min(self.fitness_mins())

    def fitness_global_max(self):
        return max(self.fitness_maxs())

    def create_fitness_df(self):
        pass

    def __calculate_limits(self, gene, margin = 0, i = 0):
        center = self.gene_median(gene)[-1]

        gene_maxs = max(self.gene_maxs(gene)[i:])
        gene_mins = min(self.gene_mins(gene)[i:])

        diameter = max(abs(gene_maxs - center), abs(gene_mins - center))
        if not isinstance(margin, int):
            margin = margin[i]

        min_val = center - (1 + margin) * diameter
        max_val = center + (1 + margin) * diameter

        return min_val, max_val


    def draw(self, i, ax, x_gene, y_gene, s, alpha, cmap, fmin, fmax):
        x = self.data["genes"][i][x_gene]
        y = self.data["genes"][i][y_gene]
        fitness_score = self.data["fitness"][i]

        # Set the range and domain of the image
        x_range = self.gene_global_max(x_gene) - self.gene_global_min(x_gene)
        y_range = self.gene_global_max(y_gene) - self.gene_global_min(y_gene)
        ax.set_xlim(self.gene_global_min(x_gene) - 0.1 * x_range, self.gene_global_max(x_gene) + 0.1 * x_range)
        ax.set_ylim(self.gene_global_min(y_gene) - 0.1 * y_range, self.gene_global_max(y_gene) + 0.1 * y_range)

        ax.scatter(x, y, c = fitness_score, s = s, alpha = alpha, cmap = cmap, vmin = fmin, vmax = fmax)

    def draw_inset(self, i, ax1, ax2, x_gene, y_gene, s, alpha, cmap, fmin, fmax, inset):

        self.draw(i, ax1, x_gene, y_gene, s, alpha, cmap, fmin, fmax)
        # set up the bounds for the inset
        x_min = inset[0]
        x_max = inset[1]
        y_min = inset[2]
        y_max = inset[3]

        ax2.set_xlim(x_min, x_max)
        ax2.set_ylim(y_min, y_max)

        x = self.data["genes"][i][x_gene]
        y = self.data["genes"][i][y_gene]
        fitness_score = self.data["fitness"][i]

        mark_inset(ax1, ax2, loc1=2, loc2=3, ec='k')

        ax2.scatter(x, y, c=fitness_score, s=s, alpha=alpha, cmap=cmap, vmin = fmin, vmax = fmax)


    def animate(self, x_gene, y_gene, s = 5, alpha = 0.5, fps = 30, log_scale = False, fmin = None, fmax = None, cmap = cm.rainbow, optimum = [], inset = False):

        plt.clf()

        if inset is False:
            fig = plt.figure(figsize=(6, 5))
            ax1 = fig.add_subplot(111)
        else:
            fig = plt.figure(figsize=(6, 3))
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            ax2.set_xlabel(x_gene)
            ax2.set_ylabel(y_gene)


        fig.subplots_adjust(left=0.12, bottom=0.2, right=0.92, top=0.93, wspace=0.4, hspace=None)
        ax1.set_xlabel(x_gene)
        ax1.set_ylabel(y_gene)


        # Set the range and domain of the image
        x_range = self.gene_global_max(x_gene) - self.gene_global_min(x_gene)
        y_range = self.gene_global_max(y_gene) - self.gene_global_min(y_gene)

        ax1.set_xlim(self.gene_global_min(x_gene) - 0.1 * x_range, self.gene_global_max(x_gene) + 0.1 * x_range)
        ax1.set_ylim(self.gene_global_min(y_gene) - 0.1 * y_range, self.gene_global_max(y_gene) + 0.1 * y_range)

        # plot optimum
        if len(optimum) > 0:
            ax1.scatter(optimum[0], optimum[1], s=5 * s, marker='*', c='k',)
        if inset:
            ax2.scatter(optimum[0], optimum[1], s=5 * s, marker='*', c='k', )

        # Set up the colorbar range
        if fmin is None:
            fmin = self.fitness_global_min()

        if fmax is None:
            fmax = self.fitness_global_max()

        if log_scale:
            fmin = np.log(fmin)
            fmax = np.log(fmax)

        # plot invisible points to establish a colorbar
        scat = ax1.scatter([0, 0], [0, 0], c = [fmin, fmax], s = 0, vmin=fmin, vmax=fmax, cmap=cmap)


        cb = plt.colorbar(scat)
        cb.solids.set_edgecolor("face")
        if log_scale:
            cb.set_label("Fitness score (log scale)")
        else:
            cb.set_label("Fitness score")

        if inset is False:
            ani = animation.FuncAnimation(fig, self.draw, fargs = (ax1, x_gene, y_gene, s, alpha, cmap, fmin, fmax), frames = self.epochs, interval = 5, repeat = True)
        else:
            ani = animation.FuncAnimation(fig, self.draw_inset, fargs=(ax1, ax2, x_gene, y_gene, s, alpha, cmap, fmin, fmax, inset), frames=self.epochs,
                                      interval=5, repeat=True)
        ani.save("{}{}_{}_progression.gif".format(self.results_folder, x_gene, y_gene),
                 writer='imagemagick', fps=fps)

        return ani

    def plot_fitness(self):
        plt.figure()
        plt.title("Minimum fitness score")
        plt.xlabel("Epoch")
        plt.ylabel("fitness")
        plt.plot(self.fitness_mins())
        plt.savefig(fname = "{}fitness".format(self.results_folder))
        plt.show()

    def plot_diversity(self, gene = None):
        plt.figure()
        plt.title("Diversity")
        plt.plot(self.data["average_diversity"], label = "Average", linewidth = 0.5)
        for gene in self.gene_names:
            gene_div = [div[gene] for div in self.data["diversity"]]
            plt.plot(gene_div, label = gene, linewidth = 0.5)
        plt.legend()
        plt.savefig(fname="{}_diversity".format(self.results_folder))
        plt.show()

    def plot_3d(self, x_gene, y_gene, z_gene):
        pass

    def print_best(self, minimise = True):
        best = False
        for epoch in self.data["history"]:
            for ind in epoch:

                if best == False:
                    best = ind
                else:
                    if minimise:
                        if ind.fitness_score < best.fitness_score:
                            best = ind
                    else:
                        if ind.fitness_score > best.fitness_score:
                            best = ind
        for gene in self.gene_names:
            print(gene + ": {0:4e}".format(best.genes[gene]))
        print("fitness score: {0:4e}".format(best.fitness_score))
