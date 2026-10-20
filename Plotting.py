import matplotlib.pyplot as plt
import numpy as np

def plot_dome_profile(x_in, r_in, x_out, r_out, x_stop, r_stop, x_cap, r_cap, x_cap_out, r_cap_out, r_dome, polar_boss_opening):
    # Plotting the dome only (with winding angle sanity check) and exporting the dome profile to CSV for CAD

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(8, 10),
        gridspec_kw={'height_ratios': [3, 1]},   # geometry gets 3x the height
    )

    ax1.plot(x_in,  r_in,  '-', color='tab:blue', linewidth=1.5, label='Inner surface')
    ax1.plot(x_out, r_out, '-', color='tab:red',  linewidth=1.5, label='Outer surface')
    ax1.scatter([x_stop], [r_stop], color='black', zorder=5, label='Dome/cap handoff (outer)')
    ax1.scatter([x_cap[-1]],     [r_cap[-1]],     color='green', zorder=5, label='Boss opening (outer)')
    ax1.scatter([x_cap_out[-1]], [r_cap_out[-1]], color='green', marker='s', zorder=5, label='Boss opening (inner)')
    ax1.set_xlabel('Axial position x (mm)')
    ax1.set_ylabel('Radius r (mm)')
    ax1.set_title('Dome profile (geodesic dome + spherical cap)')
    ax1.set_aspect('equal')
    ax1.grid(True)
    ax1.legend()

    alpha_dome_deg = np.degrees(np.arcsin(np.clip(polar_boss_opening / r_dome, -1, 1)))
    ax2.plot(r_dome, alpha_dome_deg, '-', color='tab:orange')
    ax2.set_xlabel('Local radius r (mm)')
    ax2.set_ylabel('Winding angle (deg)')
    ax2.set_title('Winding angle along dome (sanity check)')
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('dome_profile_plot.png', dpi=150)
    plt.close(fig)
    print("Exported dome_profile_plot.png")
    
def plot_tank_profile(x_in_full, r_in_full, x_out_full, r_out_full, cylinder_length, tank_radius, thickness):
        #Tank profile plot (full tank, dome + cylinder + dome)

    # Size the figure to match the tank's proportions so the plot fills the
    # canvas instead of leaving big empty margins above and below.
    x_min = min(x_in_full.min(), x_out_full.min())
    x_max = max(x_in_full.max(), x_out_full.max())
    r_max = max(r_in_full.max(), r_out_full.max())

    fig_width = 20
    fig_height = max(fig_width * (r_max / (x_max - x_min)) + 1.0, 3.0)

    fig2, ax = plt.subplots(figsize=(fig_width, fig_height))

    ax.plot(x_in_full,  r_in_full,  '-', color='tab:blue', linewidth=1.5, label='Inner surface')
    ax.plot(x_out_full, r_out_full, '-', color='tab:red',  linewidth=1.5, label='Outer surface')

    # Tank-dome interfaces only (x = 0 and x = L), on both surfaces
    ax.scatter([0, cylinder_length], [tank_radius, tank_radius],
            color='black', zorder=5, label='Tank-dome interface')
    ax.scatter([0, cylinder_length], [tank_radius + thickness, tank_radius + thickness],
            color='black', zorder=5)

    ax.set_xlabel('Axial position x (m)')
    ax.set_ylabel('Radius r (m)')
    ax.set_title('Full tank profile')
    ax.set_aspect('equal')
    ax.margins(0.01)
    ax.grid(True)
    ax.legend(loc='center left', bbox_to_anchor=(1.01, 0.5))
    fig2.tight_layout()
    fig2.savefig('tank_profile_plot.png', dpi=200, bbox_inches='tight')
    plt.close(fig2)
    print("Exported tank_profile_plot.png")