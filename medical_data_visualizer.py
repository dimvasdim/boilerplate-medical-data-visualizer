import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
bmi = df["weight"] / ((df["height"] / 100) ** 2)
df['overweight'] =  (bmi > 25) * 1

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df["cholesterol"] = (df["cholesterol"] > 1) * 1
df["gluc"] = (df["gluc"] > 1) * 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt(id_vars = ["cardio"],
                     value_vars = ["cholesterol", "gluc", "smoke",
                     "alco", "active", "overweight"])

    # Draw the catplot with 'sns.catplot()'
    category_order = ["active", "alco", "cholesterol", "gluc", "overweight", "smoke"]
    g = sns.catplot(data=df_cat, x="variable", kind="count", hue="value",
                    col="cardio", legend=True, order=category_order)
    g.set(ylabel = "total")
    #plt.show()
    fig = g.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[(df["ap_lo"] <= df["ap_hi"]) &
                     (df["height"] >= df["height"].quantile(0.025)) &
                     (df["height"] <= df["height"].quantile(0.975)) &
                     (df["weight"] >= df["weight"].quantile(0.025)) &
                     (df["weight"] <= df["weight"].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, mask=mask, square=True, annot=True,
                     center=0, vmax=0.249, vmin=-0.099, linewidths=.5,
                     fmt='.1f', ax=ax, cbar_kws={'format': '%.2f', 'shrink': .40})
    #plt.show()

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
