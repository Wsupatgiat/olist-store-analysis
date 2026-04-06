import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_cat(df, cat_col, num_col, type=None, n=None, rank_by="sum", figsize=(20, 20)):
	grouped = df.groupby(cat_col)[num_col].agg(["sum", "mean", "count"])

	if type == "top" and n is not None:
		grouped = grouped.sort_values(rank_by, ascending=False).head(n)
	elif type == "bottom" and n is not None:
		grouped = grouped.sort_values(rank_by, ascending=True).head(n)

	fig, axes = plt.subplots(3, 2, figsize=figsize)

	grouped["sum"].plot(kind="bar", ax=axes[0, 0], title=f"Sum of {num_col} by {cat_col}")
	grouped["sum"].plot(kind="bar", ax=axes[0, 1], logy=True, title=f"Log Sum of {num_col} by {cat_col}")

	grouped["mean"].plot(kind="bar", ax=axes[1, 0], title=f"Mean of {num_col} by {cat_col}")
	grouped["mean"].plot(kind="bar", ax=axes[1, 1], logy=True, title=f"Log Mean of {num_col} by {cat_col}")

	grouped["count"].plot(kind="bar", ax=axes[2, 0], title=f"Count by {cat_col}")
	grouped["count"].plot(kind="bar", ax=axes[2, 1], logy=True, title=f"Log Count by {cat_col}")

	for ax in axes.flatten():
		ax.set_xlabel(cat_col)
		ax.tick_params(axis="x", rotation=90)

	plt.tight_layout()
	plt.show()


def plot_distribution(series, label=None, figsize=(14, 5)):
	label = label or series.name

	fig, axes = plt.subplots(1, 2, figsize=figsize)

	sns.histplot(series, bins=50, kde=True, ax=axes[0])
	axes[0].set_title(f"{label} Distribution")
	axes[0].set_xlabel(label)

	sns.histplot(np.log1p(series), bins=50, kde=True, ax=axes[1])
	axes[1].set_title(f"Log {label} Distribution")
	axes[1].set_xlabel(f"log({label})")

	plt.tight_layout()
	plt.show()




def plot_boxplot_by_group(df, cat_col, num_col, figsize=(20, 5)):
	"""Box plot and violin plot grouped by category, raw and log scale."""
	flier = dict(markeredgewidth=0, markerfacecolor="steelblue", marker="o")

	df_log = df.copy()
	df_log[num_col] = np.log1p(df_log[num_col])

	fig, axes = plt.subplots(1, 4, figsize=figsize)

	sns.boxplot(data=df, x=cat_col, y=num_col, flierprops=flier, ax=axes[0])
	axes[0].set_title(f"{num_col} by {cat_col}")
	axes[0].tick_params(axis="x", rotation=90)

	sns.boxplot(data=df_log, x=cat_col, y=num_col, flierprops=flier, ax=axes[1])
	axes[1].set_title(f"{num_col} by {cat_col} (log scale)")
	axes[1].set_ylabel(f"log({num_col})")
	axes[1].tick_params(axis="x", rotation=90)

	sns.violinplot(data=df, x=cat_col, y=num_col, ax=axes[2])
	axes[2].set_title(f"{num_col} by {cat_col} violin")
	axes[2].tick_params(axis="x", rotation=90)

	sns.violinplot(data=df_log, x=cat_col, y=num_col, ax=axes[3])
	axes[3].set_title(f"{num_col} by {cat_col} violin (log scale)")
	axes[3].set_ylabel(f"log({num_col})")
	axes[3].tick_params(axis="x", rotation=90)

	plt.tight_layout()
	plt.show()


def plot_heatmap(df, row_col, col_col, val_col, top_rows=20, top_cols=20, figsize=(16, 12)):
	"""Heatmap of top_rows x top_cols by val_col sum."""
	top_r = df.groupby(row_col)[val_col].sum().sort_values(ascending=False).head(top_rows).index
	top_c = df.groupby(col_col)[val_col].sum().sort_values(ascending=False).head(top_cols).index

	pivot = (
		df[df[row_col].isin(top_r) & df[col_col].isin(top_c)]
		.groupby([row_col, col_col])[val_col]
		.sum()
		.unstack(fill_value=0)
	)

	fig, ax = plt.subplots(figsize=figsize)
	sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.5)
	ax.set_title(f"{val_col} by {row_col} × {col_col}")
	ax.tick_params(axis="x", rotation=90)
	ax.tick_params(axis="y", rotation=0)
	plt.tight_layout()
	plt.show()


def plot_scatter(df, x_col, y_col, hue_col=None, log_y=True, figsize=(10, 6)):
	"""Scatter plot with optional hue, raw and log scale side by side."""
	df_log = df.copy()
	df_log[x_col] = np.log1p(df_log[x_col])
	if log_y:
		df_log[y_col] = np.log1p(df_log[y_col])

	fig, axes = plt.subplots(1, 2, figsize=figsize)

	sns.scatterplot(data=df, x=x_col, y=y_col, hue=hue_col, alpha=0.3, linewidth=0, ax=axes[0])
	axes[0].set_title(f"{y_col} vs {x_col}")

	sns.scatterplot(data=df_log, x=x_col, y=y_col, hue=hue_col, alpha=0.3, linewidth=0, ax=axes[1])
	axes[1].set_title(f"{y_col} vs {x_col} (log scale)")
	axes[1].set_xlabel(f"log({x_col})")
	if log_y:
		axes[1].set_ylabel(f"log({y_col})")

	plt.tight_layout()
	plt.show()


def plot_hexbin(df, x_col, y_col, log_y=False, gridsize=30, figsize=(14, 6)):
	"""Hexbin density plot, raw and log-x scale side by side."""
	fig, axes = plt.subplots(1, 2, figsize=figsize)

	# Raw
	hb0 = axes[0].hexbin(df[x_col], df[y_col], gridsize=gridsize, cmap="YlOrRd", mincnt=1)
	fig.colorbar(hb0, ax=axes[0], label="Count")
	axes[0].set_title(f"{y_col} vs {x_col}")
	axes[0].set_xlabel(x_col)
	axes[0].set_ylabel(y_col)

	# Log-x (and optionally log-y)
	x_log = np.log1p(df[x_col])
	y_log = np.log1p(df[y_col]) if log_y else df[y_col]
	hb1 = axes[1].hexbin(x_log, y_log, gridsize=gridsize, cmap="YlOrRd", mincnt=1)
	fig.colorbar(hb1, ax=axes[1], label="Count")
	axes[1].set_title(f"{y_col} vs {x_col} (log scale)")
	axes[1].set_xlabel(f"log({x_col})")
	axes[1].set_ylabel(f"log({y_col})" if log_y else y_col)

	plt.tight_layout()
	plt.show()


def plot_kde_by_group(df, cat_col, num_col, figsize=(14, 5)):
	"""Overlapping KDE curves per group, raw and log scale side by side."""
	df_plot = df.copy()
	df_plot[f"log_{num_col}"] = np.log1p(df_plot[num_col])

	fig, axes = plt.subplots(1, 2, figsize=figsize)

	sns.kdeplot(data=df_plot, x=num_col, hue=cat_col, ax=axes[0])
	axes[0].set_title(f"KDE of {num_col} by {cat_col}")

	sns.kdeplot(data=df_plot, x=f"log_{num_col}", hue=cat_col, ax=axes[1])
	axes[1].set_title(f"KDE of {num_col} by {cat_col} (log scale)")
	axes[1].set_xlabel(f"log({num_col})")

	plt.tight_layout()
	plt.show()
