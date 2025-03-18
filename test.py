from utils import process_images
import matplotlib.pyplot as plt
import numpy as np
from labellines import labelLine, labelLines

colors = ["tab:green", "tab:red", "tab:blue", "tab:purple", "tab:orange", "tab:brown", "tab:pink", "tab:gray", "tab:olive", "tab:cyan"]
names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
markers = ['o', 's', 'D', '^', 'v', '>', '<', 'p', 'P', 'X']
hatches = ['/', '\\', '|', '-', '+', 'x', 'o', 'O', '.', '*']
linestyles = ['-', '--', '-.', ':'] * 2

# matplotlib settings
plt.rcParams['font.size'] = 18
# font
plt.rcParams['font.family'] = 'Lexend'
# no spines
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.bottom'] = False
plt.rcParams['axes.spines.left'] = False
# grid
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3
# grid zorder
plt.rcParams['axes.axisbelow'] = True
# save dpi
plt.rcParams['savefig.dpi'] = 300


def main():
    # create a few test figures (bad examples)

    np.random.seed(2)
    bar_data = np.random.rand(5) * 10
    line_data = np.random.rand(4, 10) * 10
    line_data[:, -1] = np.linspace(1, 9, line_data.shape[0])
    pie_data = [1, 2, 3, 2, 1]

    # scatter data (circle with Gaussian colors)
    np.random.seed(0)
    n = 1000
    # scatter_x = np.random.normal(size=n)
    # scatter_y = np.random.normal(size=n)
    scatter_r = np.random.rand(n)
    scatter_phi = np.random.rand(n)
    scatter_x = scatter_r * np.cos(2 * np.pi * scatter_phi)
    scatter_y = scatter_r * np.sin(2 * np.pi * scatter_phi)
    scatter_c = - scatter_x**2 + scatter_y**2 + np.random.normal(size=n)*0.2
    scatter_c = (scatter_c - scatter_c.min()) / (scatter_c.max() - scatter_c.min())
    
    # bar plot
    fig, ax = plt.subplots()
    ax.bar(
        names[:len(bar_data)], bar_data, color=colors[:len(bar_data)]
    )
    # legend = ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig('test_figures/bar_plot.png')

    # line plot
    fig, ax = plt.subplots()
    for i in range(line_data.shape[0]):
        ax.plot(
            range(line_data.shape[1]), line_data[i], label=names[i], color=colors[i], lw=3
        )
    ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig('test_figures/line_plot.png')

    # scatter plot
    fig, ax = plt.subplots()
    ax.scatter(
        x=scatter_x,
        y=scatter_y,
        c=scatter_c,
        cmap='RdYlGn'
    )
    # aspect
    ax.set_aspect('equal')
    # no x or y ticks but a grid
    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)
        tick.label2.set_visible(False)
    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)
        tick.label2.set_visible(False)

    # add colorbar
    cbar = fig.colorbar(ax.collections[0], ax=ax)
    cbar.set_label('Performance')

    fig.tight_layout()
    fig.savefig('test_figures/scatter_plot.png', bbox_inches='tight')

    # pie chart
    fig, ax = plt.subplots()
    ax.pie(
        pie_data, colors=colors,
    )
    ax.legend(labels=names[:len(pie_data)], loc='upper right', bbox_to_anchor=(0, 1))
    fig.tight_layout()
    fig.savefig('test_figures/pie_chart.png')

    plt.close('all')

    in_files = ['test_figures/bar_plot.png', 'test_figures/line_plot.png', 'test_figures/scatter_plot.png', 'test_figures/pie_chart.png']

    CB_TYPE = 'deuteranopia'
    SEVERITY = 1

    # process the images
    filtered_images = process_images(in_files, CB_TYPE, SEVERITY)

    # save the processed images
    for i, img in enumerate(filtered_images):
        img.save(f'{in_files[i][:-4]}_{CB_TYPE}.png')

    # display the processed images next to the originals
    fig, axs = plt.subplots(2, len(in_files), figsize=(15, 5))
    for i, (img, filtered_img) in enumerate(zip(in_files, filtered_images)):
        axs[0, i].imshow(plt.imread(img))
        axs[0, i].axis('off')
        axs[0, i].set_title('Original', fontsize=10)
        axs[1, i].imshow(filtered_img)
        axs[1, i].axis('off')
        axs[1, i].set_title(CB_TYPE.capitalize(), fontsize=10)
    plt.tight_layout()
    plt.show()

    # improve figures (good examples)

    # reset random seed
    np.random.seed(0)

    # bar plot
    fig, ax = plt.subplots()
    ax.bar(
        names[:len(bar_data)], bar_data,
        color='tab:blue',
        edgecolor='black',
        # hatch=hatches[:len(bar_data)]
    )
    # accentuate D bar in orange
    ax.patches[3].set_facecolor('tab:orange')
    ax.patches[3].set_edgecolor('black')

    # legend = ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig('test_figures/bar_plot_better.png')

    # line plot
    fig, ax = plt.subplots()
    for i in range(line_data.shape[0]):
        ax.plot(
            range(line_data.shape[1]), line_data[i], label=names[i], color=colors[i], lw=3,
            marker=markers[i], linestyle=linestyles[i], markersize=10
        )
    ax.set_xlims = (0, 12)
    labelLines(plt.gca().get_lines(), align=False, fontsize=18, xvals=[8.999] * line_data.shape[0], zorder=2.5, outline_width=10)
    # ax.legend(loc='upper right')
    fig.tight_layout()
    fig.savefig('test_figures/line_plot_better.png')

    # scatter plot
    fig, ax = plt.subplots()
    ax.scatter(
        x=scatter_x,
        y=scatter_y,
        c=scatter_c,
        cmap='viridis'
    )
    # aspect
    ax.set_aspect('equal')
    # no x or y ticks but a grid
    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)
        tick.label2.set_visible(False)
    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)
        tick.label1.set_visible(False)
        tick.label2.set_visible(False)

    # add colorbar
    cbar = fig.colorbar(ax.collections[0], ax=ax)
    cbar.set_label('Performance')

    fig.tight_layout()
    fig.savefig('test_figures/scatter_plot_better.png', bbox_inches='tight')

    # pie chart
    fig, ax = plt.subplots()
    ax.pie(
        pie_data, colors=colors,
        # labels=names[:len(pie_data)],
        hatch=hatches[:len(pie_data)],
        wedgeprops = {'linewidth': 2,
                      'edgecolor': 'black'},
    )
    ax.legend(labels=names[:len(pie_data)], loc='upper right', bbox_to_anchor=(0, 1))
    fig.tight_layout()
    fig.savefig('test_figures/pie_chart_better.png')

    plt.close('all')

    in_files = ['test_figures/bar_plot_better.png', 'test_figures/line_plot_better.png', 'test_figures/scatter_plot_better.png', 'test_figures/pie_chart_better.png']

    # process the images
    filtered_images = process_images(in_files, CB_TYPE, SEVERITY)

    # save the processed images
    for i, img in enumerate(filtered_images):
        img.save(f'{in_files[i][:-4]}_{CB_TYPE}.png')

    # display the processed images next to the originals
    fig, axs = plt.subplots(2, len(in_files), figsize=(15, 5))
    for i, (img, filtered_img) in enumerate(zip(in_files, filtered_images)):
        axs[0, i].imshow(plt.imread(img))
        axs[0, i].axis('off')
        axs[0, i].set_title('Original', fontsize=10)
        axs[1, i].imshow(filtered_img)
        axs[1, i].axis('off')
        axs[1, i].set_title(CB_TYPE.capitalize(), fontsize=10)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()