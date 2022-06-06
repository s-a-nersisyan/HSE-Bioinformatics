from bio import *


def scatterplot(x, y, data=None, figsize=(10, 10), xlim=None, ylim=None, title=None, kde=False, save_path=None, **kwargs):
    if kde:
        ax = sns.jointplot(x=x, y=y, data=data, kind="reg", space=0, marginal_kws=dict(bins=100), height=figsize[1])
        if title: ax.fig.suptitle(title)
        if xlim: ax.ax_marg_x.set_xlim(*xlim)
        if ylim: ax.ax_marg_y.set_ylim(*ylim)
    else:
        _, ax = plt.subplots(figsize=figsize)
        if title: plt.title(title)
        sns.jointplot(x=x, y=y, data=data, ax=ax)
        if xlim: plt.xlim(xlim)
        if ylim: plt.ylim(ylim)

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    else:
        plt.show()
    plt.close()
