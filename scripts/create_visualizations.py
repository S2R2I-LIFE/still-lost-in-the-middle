#!/usr/bin/env python3
"""Create visualizations for Lost in the Middle replication results."""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Results data
oracle_scores = {
    'gemma3:4b': 0.8915,
    'mistral-small:22b': 0.8599,
    'gemma3:27b': 0.9002
}

position_scores = {
    'gemma3:4b': {
        0: 0.5879,
        4: 0.5589,
        9: 0.5552
    },
    'mistral-small:22b': {
        0: 0.6878,
        4: 0.6719,
        9: 0.6365
    },
    'gemma3:27b': {
        0: 0.6591,
        4: 0.6192,
        9: 0.6113
    }
}

closedbook_score = 0.2279

# Colors for each model
colors = {
    'gemma3:4b': '#FF6B6B',
    'mistral-small:22b': '#4ECDC4',
    'gemma3:27b': '#95E1D3'
}

##############################################################################
# Figure 1: Position vs Accuracy (Main Result)
##############################################################################

fig, ax = plt.subplots(figsize=(12, 8))

for model, scores in position_scores.items():
    positions = sorted(scores.keys())
    accuracies = [scores[p] * 100 for p in positions]

    ax.plot(positions, accuracies, marker='o', linewidth=3, markersize=12,
            label=model, color=colors[model], alpha=0.8)

    # Add value labels
    for pos, acc in zip(positions, accuracies):
        ax.annotate(f'{acc:.1f}%',
                   xy=(pos, acc),
                   xytext=(0, 10),
                   textcoords='offset points',
                   ha='center',
                   fontsize=10,
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=colors[model], alpha=0.3))

# Add oracle and closedbook reference lines
ax.axhline(y=closedbook_score * 100, color='gray', linestyle='--',
           linewidth=2, alpha=0.7, label='Closedbook (no context)')
ax.text(9.5, closedbook_score * 100 + 2, 'Closedbook\n22.8%',
        ha='right', va='bottom', fontsize=10, color='gray')

# Oracle lines
for model in position_scores.keys():
    oracle_acc = oracle_scores[model] * 100
    ax.axhline(y=oracle_acc, color=colors[model], linestyle=':',
               linewidth=1.5, alpha=0.5)
    ax.text(-0.5, oracle_acc, f'{model}\noracle\n{oracle_acc:.1f}%',
            ha='right', va='center', fontsize=9, color=colors[model])

ax.set_xlabel('Gold Document Position', fontsize=14, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
ax.set_title('Position Bias in Modern LLMs (2024): No U-Shaped Curve\n10 Total Documents',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks([0, 4, 9])
ax.set_xticklabels(['0\n(Start)', '4\n(Middle)', '9\n(End)'])
ax.set_ylim(20, 95)
ax.legend(loc='upper right', fontsize=12, framealpha=0.9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Context/results/position_vs_accuracy.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Context/results/position_vs_accuracy.png")
plt.close()

##############################################################################
# Figure 2: Performance Degradation from Oracle
##############################################################################

fig, ax = plt.subplots(figsize=(10, 7))

models = list(position_scores.keys())
x = np.arange(len(models))
width = 0.25

# Calculate degradation at each position
pos_0_degradation = [oracle_scores[m] - position_scores[m][0] for m in models]
pos_4_degradation = [oracle_scores[m] - position_scores[m][4] for m in models]
pos_9_degradation = [oracle_scores[m] - position_scores[m][9] for m in models]

bars1 = ax.bar(x - width, [d * 100 for d in pos_0_degradation], width,
               label='Position 0 (Start)', color='#2ECC71', alpha=0.8)
bars2 = ax.bar(x, [d * 100 for d in pos_4_degradation], width,
               label='Position 4 (Middle)', color='#F39C12', alpha=0.8)
bars3 = ax.bar(x + width, [d * 100 for d in pos_9_degradation], width,
               label='Position 9 (End)', color='#E74C3C', alpha=0.8)

# Add value labels on bars
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=9)

ax.set_xlabel('Model', fontsize=14, fontweight='bold')
ax.set_ylabel('Performance Degradation from Oracle (%)', fontsize=14, fontweight='bold')
ax.set_title('How Much Does Position Hurt? (Lower is Better)\nDegradation = Oracle Accuracy - Position Accuracy',
             fontsize=15, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(models, rotation=15, ha='right')
ax.legend(fontsize=11, loc='upper left')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('Context/results/degradation_from_oracle.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Context/results/degradation_from_oracle.png")
plt.close()

##############################################################################
# Figure 3: Model Comparison (All Settings)
##############################################################################

fig, ax = plt.subplots(figsize=(14, 8))

x_labels = ['Oracle\n(Upper Bound)', 'Pos 0\n(Start)', 'Pos 4\n(Middle)',
            'Pos 9\n(End)', 'Closedbook\n(Lower Bound)']
x_positions = np.arange(len(x_labels))
width = 0.25

for i, (model, color) in enumerate(colors.items()):
    values = [
        oracle_scores[model] * 100,
        position_scores[model][0] * 100,
        position_scores[model][4] * 100,
        position_scores[model][9] * 100,
        closedbook_score * 100 if model == 'gemma3:4b' else None
    ]

    # Handle closedbook (only for gemma3:4b)
    if model == 'gemma3:4b':
        bars = ax.bar(x_positions + (i - 1) * width, values, width,
                     label=model, color=color, alpha=0.8)
    else:
        bars = ax.bar(x_positions[:-1] + (i - 1) * width, values[:-1], width,
                     label=model, color=color, alpha=0.8)

    # Add value labels
    for j, (bar, val) in enumerate(zip(bars, [v for v in values if v is not None])):
        ax.text(bar.get_x() + bar.get_width()/2., val + 1,
                f'{val:.1f}%',
                ha='center', va='bottom', fontsize=9, rotation=0)

ax.set_xlabel('Experimental Setting', fontsize=14, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
ax.set_title('Comprehensive Model Comparison Across All Settings',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x_positions)
ax.set_xticklabels(x_labels)
ax.set_ylim(0, 100)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('Context/results/comprehensive_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Context/results/comprehensive_comparison.png")
plt.close()

##############################################################################
# Figure 4: Comparison with Original Paper (2023 vs 2024)
##############################################################################

fig, ax = plt.subplots(figsize=(12, 7))

# Original paper data (20-doc, positions 0, 9-10, 19)
original_mpt30b = [0.567, 0.35, 0.562]  # Estimated middle from paper
original_longchat = [0.686, 0.45, 0.550]  # Estimated middle from paper

# Our data (10-doc, positions 0, 4, 9) - normalized positions for comparison
# Map our positions to comparable scale: 0→0, 4→10, 9→19 (20-doc equivalent)
our_positions_scaled = [0, 10, 19]
our_gemma4b = [position_scores['gemma3:4b'][p] for p in [0, 4, 9]]
our_mistral22b = [position_scores['mistral-small:22b'][p] for p in [0, 4, 9]]
our_gemma27b = [position_scores['gemma3:27b'][p] for p in [0, 4, 9]]

# Plot original paper results
ax.plot([0, 10, 19], [v * 100 for v in original_mpt30b],
        marker='s', linewidth=2.5, markersize=10,
        label='MPT-30B (2023, 30B)', color='#95A5A6',
        linestyle='--', alpha=0.7)
ax.plot([0, 10, 19], [v * 100 for v in original_longchat],
        marker='s', linewidth=2.5, markersize=10,
        label='LongChat-13B (2023, 13B)', color='#7F8C8D',
        linestyle='--', alpha=0.7)

# Plot our results
ax.plot(our_positions_scaled, [v * 100 for v in our_gemma4b],
        marker='o', linewidth=3, markersize=12,
        label='Gemma3:4b (2024, 4B)', color=colors['gemma3:4b'], alpha=0.9)
ax.plot(our_positions_scaled, [v * 100 for v in our_mistral22b],
        marker='o', linewidth=3, markersize=12,
        label='Mistral-Small (2024, 22B)', color=colors['mistral-small:22b'], alpha=0.9)
ax.plot(our_positions_scaled, [v * 100 for v in our_gemma27b],
        marker='o', linewidth=3, markersize=12,
        label='Gemma3:27b (2024, 27B)', color=colors['gemma3:27b'], alpha=0.9)

ax.set_xlabel('Gold Document Position (Scaled)', fontsize=14, fontweight='bold')
ax.set_ylabel('Accuracy (%)', fontsize=14, fontweight='bold')
ax.set_title('2023 vs 2024: Has Position Bias Changed?\nOriginal Paper (20-doc) vs Our Replication (10-doc)',
             fontsize=15, fontweight='bold', pad=20)
ax.set_xticks([0, 10, 19])
ax.set_xticklabels(['Start', 'Middle', 'End'])
ax.set_ylim(30, 75)
ax.legend(fontsize=11, loc='lower left', ncol=2)
ax.grid(True, alpha=0.3)

# Add annotation
ax.text(10, 70, '2024 models:\n• Higher overall performance\n• Less dramatic middle drop\n• No clear U-shape',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3),
        fontsize=10, ha='center')

plt.tight_layout()
plt.savefig('Context/results/2023_vs_2024_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: Context/results/2023_vs_2024_comparison.png")
plt.close()

print("\n✅ All visualizations created successfully!")
print("📊 Check Context/results/ for PNG files")
