import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose


def add_year_lines(axes, positions):
	ax_list = axes if hasattr(axes, "__iter__") else [axes]
	for ax in ax_list:
		for pos in positions:
			ax.axvline(x=pos, color="gray", linestyle="--", linewidth=1)


def set_xrot(ax, rotation=90):
	plt.setp(ax.xaxis.get_majorticklabels(), rotation=rotation, ha="right")


def rolling_ma(series, window):
	return pd.Series(series).rolling(window=window, min_periods=1).mean()


def monthly_agg(df, group_col):
	agg = (
		df.groupby(["month_year", group_col])["revenue"]
		.agg(count="count", avg_revenue="mean", total_revenue="sum")
		.reset_index()
	)
	agg["month_year_str"] = agg["month_year"].astype(str)
	return agg


def plot_timeseries(month_df, groups, group_col, colors, metrics, year_boundary_positions,
                    title_suffix="", figsize=(16, 14)):
	fig, axes = plt.subplots(len(metrics), 1, figsize=figsize, sharex=True)
	for ax, (metric, title, ylabel) in zip(axes, metrics):
		for group in groups:
			subset = month_df[month_df[group_col] == group].sort_values("month_year")
			ax.plot(subset["month_year_str"], subset[metric],
			        label=group, color=colors[group], marker="o", linewidth=1.5, markersize=4)
		ax.set_title(f"{title}{title_suffix}")
		ax.set_ylabel(ylabel)
		ax.legend(title=group_col, loc="upper left")
	add_year_lines(axes, year_boundary_positions)
	axes[-1].set_xlabel("Month-Year")
	set_xrot(axes[-1])
	fig.tight_layout()
	plt.show()


def plot_stacked_pct(month_df, groups, group_col, colors, metrics, year_boundary_positions,
                     title_suffix="", figsize=(16, 14)):
	pct = month_df.copy()
	for metric, _, _ in metrics:
		totals = pct.groupby("month_year")[metric].transform("sum")
		pct[f"{metric}_pct"] = pct[metric] / totals * 100
	x = pct[pct[group_col] == groups[0]].sort_values("month_year")["month_year_str"].values
	fig, axes = plt.subplots(len(metrics), 1, figsize=figsize, sharex=True)
	for ax, (metric, title, ylabel) in zip(axes, metrics):
		ys = [pct[pct[group_col] == g].sort_values("month_year")[f"{metric}_pct"].values for g in groups]
		ax.stackplot(x, *ys, labels=groups, colors=[colors[g] for g in groups], alpha=0.8)
		ax.set_title(f"{title} Share{title_suffix}")
		ax.set_ylabel("Share (%)")
		ax.set_ylim(0, 100)
		ax.axhline(y=50, color="white", linewidth=2, alpha=0.6)
		ax.legend(title=group_col, loc="upper left", ncol=2)
	ax_list = axes if hasattr(axes, "__iter__") else [axes]
	for ax in ax_list:
		for pos in year_boundary_positions:
			ax.axvline(x=pos, color="white", linewidth=2, alpha=0.6)
	axes[-1].set_xlabel("Month-Year")
	set_xrot(axes[-1])
	fig.tight_layout()
	plt.show()


def plot_timeseries_with_ma(month_df, groups, group_col, colors, metrics, year_boundary_positions,
                            ma_window=6, legend_title=None, title_suffix="", figsize=(16, 14)):
	legend_title = legend_title or group_col
	fig, axes = plt.subplots(len(metrics), 1, figsize=figsize, sharex=True)
	for ax, (metric, title, ylabel) in zip(axes, metrics):
		for group in groups:
			subset = month_df[month_df[group_col] == group].sort_values("month_year")
			x = subset["month_year_str"].values
			vals = subset[metric].values
			ma = rolling_ma(vals, ma_window)
			ax.plot(x, vals, label=group, color=colors[group], marker="o", linewidth=1.5, markersize=4)
			ax.plot(x, ma, label=f"{group} {ma_window}M MA", color=colors[group], linewidth=2, alpha=0.6, linestyle="--")
		ax.set_title(f"{title}{title_suffix}")
		ax.set_ylabel(ylabel)
		ax.legend(title=legend_title, loc="upper left")
	add_year_lines(axes, year_boundary_positions)
	axes[-1].set_xlabel("Month-Year")
	set_xrot(axes[-1])
	fig.tight_layout()
	plt.show()


def plot_category_timeseries(cat_month_df, groups, group_col, line_colors, count_colors,
                              metrics, year_boundary_positions,
                              title_suffix="", smooth=None, show_count=True, figsize=(16, 14)):
	fig, axes = plt.subplots(len(metrics), 1, figsize=figsize, sharex=True)
	for ax, (metric, title, ylabel) in zip(axes, metrics):
		if metric == "avg_revenue":
			if show_count:
				ax2 = ax.twinx()
			for cat in groups:
				subset = cat_month_df[cat_month_df[group_col] == cat].sort_values("month_year")
				lw = 3 if cat == "Other" else 1.5
				rev_vals = rolling_ma(subset["avg_revenue"].values, smooth) if smooth else subset["avg_revenue"]
				ax.plot(subset["month_year_str"], rev_vals, color=line_colors[cat], linewidth=lw, label=cat)
				if show_count:
					cnt_vals = rolling_ma(subset["count"].values, smooth) if smooth else subset["count"]
					ax2.plot(subset["month_year_str"], cnt_vals, color=count_colors[cat], linewidth=1.2, linestyle="--")
			ax.set_ylabel("Avg Revenue")
			if show_count:
				ax2.set_ylabel("Count", color="gray")
				ax2.tick_params(axis="y", labelcolor="gray")
			ax.set_title(f"{title}{title_suffix}" + (" (dashed = count)" if show_count else ""))
			ax.legend(title=group_col, loc="upper left")
		else:
			for cat in groups:
				subset = cat_month_df[cat_month_df[group_col] == cat].sort_values("month_year")
				lw = 3 if cat == "Other" else 1.5
				vals = rolling_ma(subset[metric].values, smooth) if smooth else subset[metric]
				ax.plot(subset["month_year_str"], vals, color=line_colors[cat], linewidth=lw, label=cat)
			ax.set_title(f"{title}{title_suffix}")
			ax.set_ylabel(ylabel)
			ax.legend(title=group_col, loc="upper left")
	add_year_lines(axes, year_boundary_positions)
	axes[-1].set_xlabel("Month-Year")
	set_xrot(axes[-1])
	fig.tight_layout()
	plt.show()


def plot_decomposition(decomp_series, x_labels, year_boundary_positions, period=6, figsize=(14, 12)):
	for name, s in decomp_series.items():
		result = seasonal_decompose(s.values, model="additive", period=period, extrapolate_trend="freq")
		fig, axes = plt.subplots(4, 1, figsize=figsize, sharex=True)
		components = [
			("Observed", s.values),
			("Trend", result.trend),
			("Seasonal", result.seasonal),
			("Residual", result.resid),
		]
		for ax, (label, vals) in zip(axes, components):
			ax.plot(x_labels, vals, color="steelblue", linewidth=1.5)
			ax.set_ylabel(label)
		axes[0].set_title(f"Classical Decomposition (period={period}) {name}")
		axes[-1].set_xlabel("Month-Year")
		add_year_lines(axes, year_boundary_positions)
		set_xrot(axes[-1])
		fig.tight_layout()
		plt.show()


def plot_overview_trends(series_dict, titles, ylabels, x_labels, year_boundary_positions, figsize=(14, 12)):
	fig, axes = plt.subplots(len(series_dict), 1, figsize=figsize, sharex=True)
	for ax, (_, s), title, ylabel in zip(axes, series_dict.items(), titles, ylabels):
		vals = pd.Series(s).values.astype(float)
		ma3 = rolling_ma(vals, 3)
		ma6 = rolling_ma(vals, 6)
		ax.plot(x_labels, vals, linewidth=1.5, label="Actual")
		ax.plot(x_labels, ma3, linewidth=2, alpha=0.6, linestyle=":", label="3-month MA")
		ax.plot(x_labels, ma6, linewidth=2, alpha=0.6, linestyle=":", label="6-month MA")
		ax.set_title(title)
		ax.set_ylabel(ylabel)
		ax.legend(loc="upper left")
	add_year_lines(axes, year_boundary_positions)
	axes[-1].set_xlabel("Month-Year")
	set_xrot(axes[-1])
	fig.tight_layout()
	plt.show()


def plot_category_share_pct(cat_month, cat_groups, cat_col, cat_colors, metrics, year_boundary_positions, figsize=(16, 6)):
	for metric, title, _ in metrics:
		pct = cat_month.copy()
		totals = pct.groupby("month_year")[metric].transform("sum")
		pct[f"{metric}_pct"] = pct[metric] / totals * 100

		x = pct[pct[cat_col] == cat_groups[0]].sort_values("month_year")["month_year_str"].values
		ys = [pct[pct[cat_col] == c].sort_values("month_year")[f"{metric}_pct"].values for c in cat_groups]

		fig, ax = plt.subplots(figsize=figsize)
		ax.stackplot(x, *ys, labels=cat_groups, colors=[cat_colors[c] for c in cat_groups], alpha=0.8)
		ax.set_title(f"{title} Share: Top 7 Categories (% of top 7 only)")
		ax.set_ylabel("Share (%)")
		ax.set_xlabel("Month-Year")
		ax.legend(title=cat_col, loc="upper left", ncol=2)
		ax.set_ylim(0, 100)
		ax.axhline(y=50, color="white", linewidth=2, alpha=0.6)
		for pos in year_boundary_positions:
			ax.axvline(x=pos, color="white", linewidth=2, alpha=0.6)
		set_xrot(ax)
		fig.tight_layout()
		plt.show()


def plot_detrended(series, x_labels, year_boundary_positions, method="subtract", title="", ylabel="", label="", figsize=(14, 5)):
	vals = pd.Series(series).values.astype(float)
	ma6 = rolling_ma(vals, 6)

	if method == "subtract":
		result = vals - ma6
		ref_value = 0
	else:
		result = vals / ma6
		ref_value = 1

	fig, ax = plt.subplots(figsize=figsize)
	ax.plot(x_labels, result, linewidth=1.5, label=label)
	ax.axhline(y=ref_value, color="gray", linestyle="--", linewidth=1)
	ax.set_title(title)
	ax.set_ylabel(ylabel)
	ax.set_xlabel("Month-Year")
	if label:
		ax.legend(loc="upper left")
	add_year_lines(ax, year_boundary_positions)
	set_xrot(ax)
	fig.tight_layout()
	plt.show()


def plot_state_category_hexbin(df, metric, title, cbar_label, reduce_fn, figsize=(16, 10)):
	agg = df.groupby(["state", "category"])["revenue"].agg(count="count", mean="mean", total="sum").reset_index()

	state_order = agg.groupby("state")[metric].sum().sort_values(ascending=False).index.tolist()
	category_order = agg.groupby("category")[metric].sum().sort_values(ascending=False).index.tolist()

	state_map = {s: i for i, s in enumerate(state_order)}
	category_map = {c: i for i, c in enumerate(category_order)}

	df_plot = df.copy()
	df_plot["state_code"] = df_plot["state"].map(state_map)
	df_plot["category_code"] = df_plot["category"].map(category_map)

	fig, ax = plt.subplots(figsize=figsize)
	hb = ax.hexbin(df_plot["state_code"], df_plot["category_code"],
	               C=df_plot["revenue"] if metric != "count" else None,
	               gridsize=(len(state_map), len(category_map)),
	               cmap="YlOrRd", mincnt=1,
	               reduce_C_function=reduce_fn)
	fig.colorbar(hb, ax=ax, label=cbar_label)
	ax.set_title(f"State x Category: {title} (ranked by {metric})")
	ax.set_xticks(range(len(state_map)))
	ax.set_xticklabels(state_order, rotation=90)
	ax.set_yticks(range(len(category_map)))
	ax.set_yticklabels(category_order, fontsize=7)
	ax.set_xlabel("State (ranked by metric)")
	ax.set_ylabel("Category (ranked by metric)")
	fig.tight_layout()
	plt.show()


def plot_state_category_heatmap(df, metric, title, cbar_label, figsize=(16, 10)):
	agg = df.groupby(["state", "category"])["revenue"].agg(count="count", mean="mean", total="sum").reset_index()

	state_order = agg.groupby("state")[metric].sum().sort_values(ascending=False).index.tolist()
	category_order = agg.groupby("category")[metric].sum().sort_values(ascending=False).index.tolist()

	pivot = agg.pivot(index="category", columns="state", values=metric)
	pivot = pivot.reindex(index=category_order, columns=state_order)

	fig, ax = plt.subplots(figsize=figsize)
	im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
	fig.colorbar(im, ax=ax, label=cbar_label)
	ax.set_title(f"State x Category: {title} (ranked by {metric})")
	ax.set_xticks(range(len(state_order)))
	ax.set_xticklabels(state_order, rotation=90)
	ax.set_yticks(range(len(category_order)))
	ax.set_yticklabels(category_order)
	ax.set_xlabel("State (ranked by metric)")
	ax.set_ylabel("Category (ranked by metric)")
	fig.tight_layout()
	plt.show()
