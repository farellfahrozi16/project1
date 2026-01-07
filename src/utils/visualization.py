import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
import numpy as np
from typing import Dict, List

class PostureVisualizer:
    @staticmethod
    def create_shoulder_plot(shoulder_imbalance: float) -> Figure:
        fig = Figure(figsize=(3, 3), facecolor='white')
        ax = fig.add_subplot(111)

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title('ANALISIS SUDUT BAHU', fontsize=10, fontweight='bold')
        ax.set_xlabel('')
        ax.set_ylabel('')

        left_y = 5
        right_y = 5 - (shoulder_imbalance / 10)

        ax.plot([2, 8], [left_y, right_y], 'b-', linewidth=3, label=f'Slope: {shoulder_imbalance/10:.1f}°')
        ax.scatter([2, 8], [left_y, right_y], c='blue', s=100, zorder=5)

        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)

        return fig

    @staticmethod
    def create_hip_plot(hip_imbalance: float) -> Figure:
        fig = Figure(figsize=(3, 3), facecolor='white')
        ax = fig.add_subplot(111)

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title('ANALISIS SUDUT PINGGUL', fontsize=10, fontweight='bold')

        left_y = 5
        right_y = 5 - (hip_imbalance / 10)

        ax.plot([2, 8], [left_y, right_y], 'g-', linewidth=3, label=f'Pelvic Tilt: {hip_imbalance/10:.1f}°')
        ax.scatter([2, 8], [left_y, right_y], c='green', s=100, zorder=5)

        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)

        return fig

    @staticmethod
    def create_spine_plot(spine_deviation: float) -> Figure:
        fig = Figure(figsize=(3, 3), facecolor='white')
        ax = fig.add_subplot(111)

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title('ANALISIS SUDUT TULANG BELAKANG', fontsize=10, fontweight='bold')

        center_x = 5
        deviation_x = center_x + (spine_deviation / 20)

        ax.plot([center_x, deviation_x], [2, 8], 'purple', linewidth=3, label=f'Curvature: {spine_deviation/10:.1f}°')
        ax.axvline(x=center_x, color='gray', linestyle='--', alpha=0.5)

        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)

        return fig

    @staticmethod
    def create_head_tilt_plot(head_tilt: float) -> Figure:
        fig = Figure(figsize=(3, 3), facecolor='white')
        ax = fig.add_subplot(111)

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title('ANALISIS SUDUT KEPALA', fontsize=10, fontweight='bold')

        center_x = 5
        center_y = 6

        angle_rad = np.radians(head_tilt)
        end_x = center_x + 2 * np.cos(angle_rad)
        end_y = center_y + 2 * np.sin(angle_rad)

        ax.plot([center_x, end_x], [center_y, end_y], 'b-', linewidth=3, label=f'Head Tilt: {head_tilt:.1f}°')
        ax.scatter([center_x], [center_y], c='blue', s=100, zorder=5)

        ax.legend(loc='upper right', fontsize=8)
        ax.grid(True, alpha=0.3)

        return fig

    @staticmethod
    def create_foot_plot() -> Figure:
        fig = Figure(figsize=(3, 3), facecolor='white')
        ax = fig.add_subplot(111)

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title('ANALISIS SUDUT KAKI', fontsize=10, fontweight='bold')

        ax.plot([3, 7], [5, 5], 'r-', linewidth=3)
        ax.scatter([3, 7], [5, 5], c='red', s=100, zorder=5)

        ax.grid(True, alpha=0.3)

        return fig

    @staticmethod
    def create_scapular_plot(scapular_angle: float) -> Figure:
        fig = Figure(figsize=(3, 3), facecolor='white')
        ax = fig.add_subplot(111)

        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_title('RINGKASAN SUDUT POSTURAL', fontsize=10, fontweight='bold')

        ax.text(5, 5, f'Scapular Angle: {scapular_angle:.1f}°',
               ha='center', va='center', fontsize=12, fontweight='bold')

        ax.grid(True, alpha=0.3)

        return fig
