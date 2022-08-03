from bio import *


def clustermap(df, show=False, save_path=None, ax=None, **kwargs):
    cg = sns.clustermap(
        df,
        **{
            'cmap': sns.color_palette("bwr", as_cmap=True),
            **kwargs,
        },
        ax=ax,
    )

    cg.ax_heatmap.yaxis.tick_left()
    plt.setp(cg.ax_heatmap.yaxis.get_majorticklabels(), rotation=0)
    
    if save_path:
        cg.savefig(save_path, dpi=300)
    if show:
        plt.show()
        
    plt.close()
