import numpy as np
# https://github.com/usnistgov/atomman
import atomman as am
from ase.lattice.cubic import BodyCenteredCubic
from ase.constraints import FixAtoms, StrainFilter
from ase.optimize import FIRE
from ase.build import bulk
from matscipy.elasticity import fit_elastic_constants
from ase.calculators.lammpslib import LAMMPSlib
from ase.units import GPa  # unit convertion
from ase.lattice.cubic import SimpleCubicFactory

from matscipy.neighbours import neighbour_list, mic


def make_screw_cyl(alat, C11, C12, C44,
                   cylinder_r=10, cutoff=5.5,
                   hard_core=False,
                   center=(0., 0., 0.),
                   l_extend=(0., 0., 0.),
                   symbol='W'):

    """Makes screw dislocation using atomman library

    Parameters
    ----------
    alat : float
        Lattice constant of the material.
    C11 : float
        C11 elastic constant of the material.
    C12 : float
        C12 elastic constant of the material.
    C44 : float
        C44 elastic constant of the material.
    cylinder_r : float
        radius of cylinder of unconstrained atoms around the
        dislocation  in angstrom
    cutoff : float
        Potential cutoff for marinica potentials for FS cutoff = 4.4
    hard_core : bool
        Description of parameter `hard_core`.
    center : type
        The position of the dislocation core and the center of the
                 cylinder with FixAtoms condition
    l_extend : float
        extention of the box. used for creation of initial
        dislocation position with box equivalent to the final position
    symbol : string
        Symbol of the element to pass to ase.lattuce.cubic.SimpleCubicFactory
        default is "W" for tungsten

    Returns
    -------
    disloc : ase.Atoms object
        screw dislocation cylinder.
    bulk : ase.Atoms object
        bulk disk used to generate dislocation
    u : np.array
        displacement per atom.
    """
    # Create a Stroh ojbect with junk data
    stroh = am.defect.Stroh(am.ElasticConstants(C11=141, C12=110, C44=98),
                            np.array([0, 0, 1]))

    axes = np.array([[1, 1, -2],
                     [-1, 1, 0],
                     [1, 1, 1]])

    c = am.ElasticConstants(C11=C11, C12=C12, C44=C44)
    burgers = alat * np.array([1., 1., 1.])/2.

    # Solving a new problem with Stroh.solve
    stroh.solve(c, burgers, axes=axes)

    # test the solution that it does not crash
    # pos_test = uc.set_in_units(np.array([12.4, 13.5, -10.6]), 'angstrom')
    # disp = stroh.displacement(pos_test)
    # print("displacement =", uc.get_in_units(disp, 'angstrom'), 'angstrom')

    unit_cell = BodyCenteredCubic(directions=axes.tolist(),
                                  size=(1, 1, 1), symbol=symbol,
                                  pbc=(False, False, True),
                                  latticeconstant=alat)

    # make the dislocation core center of the box
    disloCenterX = alat * np.sqrt(6.)/6.0
    disloCenterY = alat * np.sqrt(2.)/6.0

    unit_cell.positions[:, 0] -= disloCenterX
    unit_cell.positions[:, 1] -= disloCenterY

    # shift to move the fixed atoms boundary condition for the
    # configuration with shifted dislocation core
    shift_x = 2.0 * center[0]
    shift_y = 2.0 * center[1]

    l_shift_x = 2.0 * l_extend[0]
    l_shift_y = 2.0 * l_extend[1]

    # size of the cubic cell as a 112 direction
    Lx = int(round((cylinder_r + 3.*cutoff + shift_x + l_shift_x)
                   / (alat * np.sqrt(6.))))

    # size of the cubic cell as a 110 direction
    Ly = int(round((cylinder_r + 3.*cutoff + shift_y + l_shift_y)
                   / (alat * np.sqrt(2.))))
    # factor 2 to make shure odd number of images is translated
    # it is important for the correct centering of the dislocation core
    bulk = unit_cell * (2*Lx, 2*Ly, 1)
    # make 0, 0, at the center
    bulk.positions[:, 0] -= Lx * alat * np.sqrt(6.)
    bulk.positions[:, 1] -= Ly * alat * np.sqrt(2.)

    # wrap
    # bulk.set_scaled_positions(bulk.get_scaled_positions())
    # apply shear here:
    # bulk.cell *= D
    # bulk.positions *= D

    x, y, z = bulk.positions.T

    radius_x_y_zero = np.sqrt(x**2 + y**2)
    mask_zero = radius_x_y_zero < cylinder_r + 2.*cutoff

    radius_x_y_center = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    mask_center = radius_x_y_center < cylinder_r + 2.*cutoff

    radius_x_y_l_shift = np.sqrt((x - l_extend[0])**2 + (y - l_extend[1])**2)
    mask_l_shift = radius_x_y_l_shift < cylinder_r + 2.*cutoff

    final_mask = mask_center | mask_zero | mask_l_shift
    # leave only atoms inside the cylinder
    bulk = bulk[final_mask]

    disloc = bulk.copy()
    # calculate and apply the displacements for atomic positions
    u = stroh.displacement(bulk.positions - center)
    u = -u if hard_core else u

    disloc.positions += u
    x, y, z = disloc.positions.T

    radius_x_y_zero = np.sqrt(x**2 + y**2)
    mask_zero = radius_x_y_zero > cylinder_r

    radius_x_y_center = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    mask_center = radius_x_y_center > cylinder_r

    radius_x_y_l_shift = np.sqrt((x - l_extend[0])**2 + (y - l_extend[1])**2)
    mask_l_shift = radius_x_y_l_shift > cylinder_r

    fix_mask = mask_center & mask_zero & mask_l_shift
    # leave only atoms inside the cylinder
    fix_atoms = FixAtoms(mask=fix_mask)
    disloc.set_constraint(fix_atoms)

    # make an "region" array to map bulk and fixed atoms
    # all atoms are "MM" by default
    region = np.full_like(disloc, "MM")
    region[fix_mask] = np.full_like(disloc[fix_mask], "fixed")
    disloc.new_array("region", region)

    return disloc, bulk, u


def make_edge_cyl(alat, C11, C12, C44,
                  cylinder_r=10, cutoff=5.5,
                  symbol='W'):
    '''
    makes edge dislocation using atomman library

    cylinder_r - radius of cylinder of unconstrained atoms around the
                 dislocation  in angstrom

    cutoff - potential cutoff for marinica potentials for FS cutoff = 4.4

    symbol : string
        Symbol of the element to pass to ase.lattuce.cubic.SimpleCubicFactory
        default is "W" for tungsten
    '''

    # Create a Stroh ojbect with junk data
    stroh = am.defect.Stroh(am.ElasticConstants(C11=141, C12=110, C44=98),
                            np.array([0, 0, 1]))

    axes = np.array([[1, 1, 1],
                     [1, -1, 0],
                     [1, 1, -2]])

    c = am.ElasticConstants(C11=C11, C12=C12, C44=C44)
    burgers = alat * np.array([1., 1., 1.])/2.

    # Solving a new problem with Stroh.solve
    # Does not work with the new version of atomman
    stroh.solve(c, burgers, axes=axes)

    unit_cell = BodyCenteredCubic(directions=axes.tolist(),
                                  size=(1, 1, 1), symbol='W',
                                  pbc=(False, False, True),
                                  latticeconstant=alat)

    bulk = unit_cell.copy()

    # shift to make the zeros of the cell betweem the atomic planes
    # and under the midplane on Y axes
    X_midplane_shift = (1.0/3.0)*alat*np.sqrt(3.0)/2.0
    Y_midplane_shift = 0.25*alat*np.sqrt(2.0)

    bulk_shift = [X_midplane_shift,
                  Y_midplane_shift,
                  0.0]

    bulk.positions += bulk_shift

    tot_r = cylinder_r + cutoff + 0.01

    Lx = int(round(tot_r/(alat*np.sqrt(3.0)/2.0)))
    Ly = int(round(tot_r/(alat*np.sqrt(2.))))

    # factor 2 to make shure odd number of images is translated
    # it is important for the correct centering of the dislocation core
    bulk = bulk * (2*Lx, 2*Ly, 1)

    center_shift = [Lx * alat * np.sqrt(3.0)/2.,
                    Ly * alat * np.sqrt(2.),
                    0.0]

    bulk.positions -= center_shift

    ED = bulk.copy()

    disp = stroh.displacement(ED.positions)

    ED.positions += disp

    x, y, z = ED.positions.T
    radius_x_y_zero = np.sqrt(x**2 + y**2)
    mask = radius_x_y_zero < tot_r

    ED = ED[mask]
    bulk = bulk[mask]

    bulk.write("before.xyz")

    ED.write("after_disp.xyz")

    x, y, z = ED.positions.T
    radius_x_y_zero = np.sqrt(x**2 + y**2)
    mask_zero = radius_x_y_zero > cylinder_r
    fix_atoms = FixAtoms(mask=mask_zero)

    ED.set_constraint(fix_atoms)

    x, y, z = bulk.positions.T
    # move lower left segment
    bulk.positions[(y < 0.0) & (x < X_midplane_shift)] -= \
        [alat * np.sqrt(3.0) / 2.0, 0.0, 0.0]
    # make the doslocation extraplane center
    bulk.positions += [(1.0/3.0)*alat*np.sqrt(3.0)/2.0, 0.0, 0.0]

    return ED, bulk


def plot_vitek(dislo, bulk, show=True, save_file=None,
               alat=3.16, plot_axes=None, xyscale=10):
    """Plots vitek map from ase configurations.

    Parameters
    ----------
    dislo : ase.Atoms
        Dislocation configuration.
    bulk : ase.Atoms
        Corresponding bulk configuration for calculation of displacements.
    show : bool
        Show the figure after plotting. Default is True.
    save_file : str, optional
        If given then the plot will be saved to a file with this name.
    alat : float
        Lattice parameter for calculation of neghbour list cutoff.
    plot_axes : matplotlib.Axes.axes object
        Existing axes to plot on, allows to pass existing matplotlib axes
        have full control of the graph outside the function.
        Makes possible to plot multiple differential displacement
        maps using subplots.
        Default is None, then new graph is created by plt.subplots()
        Description of parameter `plot_axes`.
    xyscale : float
        xyscale of the graph

    Returns
    -------
    None

    """

    lengthB = 0.5*np.sqrt(3.)*alat
    burgers = np.array([0.0, 0.0, lengthB])

    base_system = am.load("ase_Atoms", bulk)
    disl_system = am.load("ase_Atoms", dislo)

    neighborListCutoff = 0.95 * alat

    # plot window is +-10 angstroms in x,y directions, and one Burgerx vector
    # thickness along z direction
    plot_range = np.array([[-xyscale, xyscale],
                          [-xyscale, xyscale],
                          [-0.1, alat * 3.**(0.5) / 2.]])

    # This scales arrows such that b/2 corresponds to the
    # distance between atoms on the plot
    plot_scale = 1.885618083

    am.defect.differential_displacement(base_system, disl_system,
                                        burgers,
                                        cutoff=neighborListCutoff,
                                        xlim=plot_range[0],
                                        ylim=plot_range[1],
                                        zlim=plot_range[2],
                                        plot_scale=plot_scale,
                                        show=show, save_file=save_file,
                                        plot_axes=plot_axes)

    return None


def show_NEB_configurations(images, bulk, xyscale=7,
                            show=True, core_positions=None):
    """Plots Vitek differential displacement maps for the list of images
       for example along the NEB path.

    Parameters
    ----------
    images : list of ase.Atoms
        List of configurations with dislocations.
    bulk : ase.Atoms
        Corresponding bulk configuration for calculation of displacements.
    xyscale : float
        xyscale of the graph
    show : bool
        Show the figure after plotting. Default is True.
    core_positions : list
        [x, y] position of dislocation core to plot

    Returns
    -------
    figure
        If the show is False else returns None

    """

    import matplotlib.pyplot as plt
    n_images = len(images)
    fig2 = plt.figure(figsize=(n_images * 4, 4))

    for i, image in enumerate(images):
        ax1 = fig2.add_subplot("1%i%i" % (n_images, i+1))
        plot_vitek(image, bulk, plot_axes=ax1, xyscale=xyscale)
        if core_positions is not None:
            x, y = core_positions[i]
            ax1.scatter(x, y, marker="+", s=200, c='C1')
    if show:
        plt.show(fig2)
        return None
    else:
        return fig2


def show_configuration(disloc, bulk, u, fixed_mask=None):
    '''
    shows the displacement fixed atoms
    '''

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(16, 4))

    ax1 = fig.add_subplot(131)
    ax1.set_title("z displacement, $\AA$")
    sc = ax1.scatter(bulk.positions[:, 0], bulk.positions[:, 1], c=u.T[2])
    ax1.axvline(0.0, color="red", linestyle="dashed")
    ax1.set_xlabel("x, $\AA$")
    ax1.set_ylabel("y, $\AA$")
    plt.colorbar(sc)

    ax2 = fig.add_subplot(132)
    ax2.set_title("x displacement, $\AA$")
    sc = ax2.scatter(bulk.positions[:, 0], bulk.positions[:, 1], c=u.T[0])
    ax2.set_xlabel("x, $\AA$")
    ax2.set_ylabel("y, $\AA$")
    plt.colorbar(sc, format="%.1e")

    ax3 = fig.add_subplot(133)
    ax3.set_title("y displacement, $\AA$")
    sc = ax3.scatter(bulk.positions[:, 0], bulk.positions[:, 1], c=u.T[1])
    plt.colorbar(sc, format="%.1e")
    ax3.set_xlabel("x, $\AA$")
    ax3.set_ylabel("y, $\AA$")

    if fixed_mask is not None:

        ax1.scatter(bulk.positions[fixed_mask, 0],
                    bulk.positions[fixed_mask, 1], c="k")

        ax2.scatter(bulk.positions[fixed_mask, 0],
                    bulk.positions[fixed_mask, 1], c="k")

        ax3.scatter(bulk.positions[fixed_mask, 0],
                    bulk.positions[fixed_mask, 1], c="k")

    plt.show()

    return None


def get_elastic_constants(pot_path=None,
                          calculator=None,
                          delta=1e-2,
                          symbol="W"):
    """
    return lattice parameter, and cubic elastic constants: C11, C12, 44
    using matscipy function
    pot_path - path to the potential

    symbol : string
        Symbol of the element to pass to ase.lattuce.cubic.SimpleCubicFactory
        default is "W" for tungsten
    """

    unit_cell = bulk(symbol)

    if (pot_path is not None) and (calculator is None):
        # create lammps calculator with the potential
        lammps = LAMMPSlib(lmpcmds=["pair_style eam/fs",
                           "pair_coeff * * %s W" % pot_path],
                           atom_types={'W': 1}, keep_alive=True)
        calculator = lammps

    unit_cell.set_calculator(calculator)

#   simple calculation to get the lattice constant and cohesive energy
#    alat0 = W.cell[0][1] - W.cell[0][0]
    sf = StrainFilter(unit_cell)  # or UnitCellFilter(W) -> to minimise wrt pos, cell
    opt = FIRE(sf)
    opt.run(fmax=1e-4)  # max force in eV/A
    alat = unit_cell.cell[0][1] - unit_cell.cell[0][0]
#    print("a0 relaxation %.4f --> %.4f" % (a0, a))
#    e_coh = W.get_potential_energy()
#    print("Cohesive energy %.4f" % e_coh)

    Cij, Cij_err = fit_elastic_constants(unit_cell,
                                         symmetry="cubic",
                                         delta=delta)

    Cij = Cij/GPa  # unit conversion to GPa

    elasticMatrix3x3 = Cij[:3, :3]
    # average of diagonal elements: C11, C22, C33
    C11 = elasticMatrix3x3.diagonal().mean()
    # make mask to extract non diagonal elements
    mask = np.ones((3, 3), dtype=bool)
    np.fill_diagonal(mask, False)

    # average of all non diagonal elements from 1 to 3
    C12 = elasticMatrix3x3[mask].mean()

    # average of diagonal elements from 4 till 6: C44, C55, C66,
    C44 = Cij[3:, 3:].diagonal().mean()

    # A = 2.*C44/(C11 - C12)

    if (pot_path is not None) and (calculator is None):
        lammps.lmp.close()

    return alat, C11, C12, C44


def make_barrier_configurations(pot_path=None, calculator=None,
                                cylinder_r=10, hard_core=False):
    """ Creates the initial and final configurations for the NEB calculation
        The positions in FixedAtoms contrained region are average between
        final and inital configurations

    Parameters
    ----------
    pot_path : sting
        Path to the potential file.
    calculator : type
        Description of parameter `calculator`.
    cylinder_r : float
        Radius of cylinder of unconstrained atoms around the
                    dislocation  in angstrom.
    hard_core : bool
        Type of the core hard or soft.
        If hard is chosen the displacment field is teversed.

    Returns
    -------
    disloc_ini : ase.Atoms
        Initial dislocation configuration.
    disloc_fin : ase.Atoms
        Final dislocation configuration.
    bulk : ase.Atoms
        Perfect bulk configuration for Vitek displacement maps

    """

    if pot_path is not None:
        alat, C11, C12, C44 = get_elastic_constants(pot_path=pot_path)
        # get the cutoff from the potential file
        with open(pot_path) as potfile:
            for i, tmp_str in enumerate(potfile):
                if i == 4:  # read the last number in the fifth line
                    cutoff = float(tmp_str.split()[-1])
                    break

    elif calculator is not None:
        alat, C11, C12, C44 = get_elastic_constants(calculator=calculator)
        cutoff = 5.0  # the value for trainig data for GAP from paper

    cent_x = np.sqrt(6.0)*alat/3.0
    center = (cent_x, 0.0, 0.0)

    disloc_ini, bulk_ini, __ = make_screw_cyl(alat, C11, C12, C44,
                                              cylinder_r=cylinder_r,
                                              cutoff=cutoff,
                                              hard_core=hard_core,
                                              l_extend=center)

    disloc_fin, __, __ = make_screw_cyl(alat, C11, C12, C44,
                                        cylinder_r=cylinder_r,
                                        cutoff=cutoff,
                                        hard_core=hard_core,
                                        center=center)

    # get the fixed atoms constrain
    FixAtoms = disloc_ini.constraints[0]
    # get the indices of fixed atoms
    fixed_atoms_indices = FixAtoms.get_indices()

    # make the average position of fixed atoms
    # between initial and the lastlast position
    ini_fix_pos = disloc_ini.get_positions()[fixed_atoms_indices]
    fin_fix_pos = disloc_fin.get_positions()[fixed_atoms_indices]

    new_av_pos = (ini_fix_pos + fin_fix_pos)/2.0

    positions = disloc_ini.get_positions()
    positions[fixed_atoms_indices] = new_av_pos
    disloc_ini.set_positions(positions, apply_constraint=False)

    positions = disloc_fin.get_positions()
    positions[fixed_atoms_indices] = new_av_pos
    disloc_fin.set_positions(positions, apply_constraint=False)

    return disloc_fin, disloc_ini, bulk_ini


def compare_configurations(dislo, bulk, dislo_ref, bulk_ref,
                           alat, cylinder_r=None, print_info=True):
    """Compares two dislocation configurations based on the gradient of
       the displacements along the bonds.

    Parameters
    ----------
    dislo : ase.Atoms
        Dislocation configuration.
    bulk : ase.Atoms
        Corresponding bulk configuration for calculation of displacements.
    dislo_ref : ase.Atoms
        Reference dislocation configuration.
    bulk_ref : ase.Atoms
        Corresponding reference bulk configuration
        for calculation of displacements.
    alat : float
        Lattice parameter for calculation of neghbour list cutoff.
    cylinder_r : float or None
        Radius of region of comparison around the dislocation coreself.
        If None makes global comparison based on the radius of
        `dislo` configuration, else compares the regions with `cylinder_r`
        around the dislocation core position.
    print_info : bool
        Flag to switch print statement about the type of the comparison
    Returns
    -------
    float
        The Du norm of the differences per atom.

    """

    if cylinder_r is None:
        x, y, __ = bulk.positions.T
        radius = np.sqrt(x**2 + y**2)
        cutoff_radius = radius.max() - 10.

        if print_info:
            print("Making a global comparison with radius %.2f" % cutoff_radius)

    else:
        cutoff_radius = cylinder_r
        if print_info:
            print("Making a local comparison with radius %.2f" % cutoff_radius)

    x, y, __ = bulk_ref.positions.T
    radius = np.sqrt(x**2 + y**2)
    cutoff_mask = (radius < cutoff_radius)

    second_NN_distance = alat
    bulk_i, bulk_j = neighbour_list('ij', bulk_ref, second_NN_distance)

    I_core, J_core = np.array([(i, j) for i, j in zip(bulk_i, bulk_j) if cutoff_mask[i]]).T

    mapping = {}

    for i in range(len(bulk)):
        mapping[i] = np.linalg.norm(bulk_ref.positions -
                                    bulk.positions[i], axis=1).argmin()

    u_ref = dislo_ref.positions - bulk_ref.positions

    u = dislo.positions - bulk.positions
    u_extended = np.zeros(u_ref.shape)
    u_extended[mapping.values(), :] = u

    du = u_extended - u_ref

    Du = np.linalg.norm(np.linalg.norm(mic(du[J_core, :] - du[I_core, :],
                                           bulk.cell), axis=1))
    return Du


def cost_function(pos, dislo, bulk, cylinder_r, elastic_param,
                  print_info=True):
    """Cost function for fitting analytical displacement field
       and detecting dislcoation core position. Uses `compare_configurations`
       function for the minisation of the core position.

    Parameters
    ----------
    pos : list of float
        Positions of the core to build the analytical solution [x, y].
    dislo : ase.Atoms
        Dislocation configuration.
    bulk : ase.Atoms
        Corresponding bulk configuration for calculation of displacements.
    cylinder_r : float or None
        Radius of region of comparison around the dislocation coreself.
        If None makes global comparison based on the radius of
        `dislo` configuration, else compares the regions with `cylinder_r`
        around the dislocation core position.
    elastic_param : list of float
        List containing alat, C11, C12, C44
    print_info : bool
        Flag to switch print statement about the type of the comparison

    Returns
    -------
    float
        Error for optimisation (result from `compare_configurations` function)

    """


    # Create a Stroh ojbect with junk data
    stroh = am.defect.Stroh(am.ElasticConstants(C11=141, C12=110, C44=98),
                            np.array([0, 0, 1]))

    axes = np.array([[1, 1, -2],
                    [-1, 1, 0],
                    [1, 1, 1]])

    alat, C11, C12, C44 = elastic_param

    c = am.ElasticConstants(C11=C11, C12=C12, C44=C44)
    burgers = alat * np.array([1., 1., 1.])/2.

    # Solving a new problem with Stroh.solve
    stroh.solve(c, burgers, axes=axes)

    center = (pos[0], pos[1], 0.0)
    u = stroh.displacement(bulk.positions - center)

    dislo_guess = bulk.copy()
    dislo_guess.positions += u

    err = compare_configurations(dislo, bulk,
                                 dislo_guess, bulk,
                                 alat, cylinder_r=cylinder_r,
                                 print_info=print_info)

    return err


def screw_cyl_tetrahedral(alat, C11, C12, C44,
                          scan_r=15,
                          symbol="W",
                          imp_symbol='H',
                          hard_core=False,
                          center=(0., 0., 0.)):
    """Generates a set of terahedral positions with `scan_r` radius.
       Applies the screw dislocation displacement for creating an initial guess
       for the H positions at dislocation core.

    Parameters
    ----------
    alat : float
        Lattice constant of the material.
    C11 : float
        C11 elastic constant of the material.
    C12 : float
        C12 elastic constant of the material.
    C44 : float
        C44 elastic constant of the material.
    scan_r : float
        Radius of the region to create tetrahedral positions.
    symbol : string
        Symbol of the element to pass to ase.lattuce.cubic.SimpleCubicFactory
        default is "W" for tungsten
    imp_symbol : string
        Symbol of the elemnt to pass creat Atoms object
        default is "H" for hydrogen
    hard_core : float
        Type of the dislocatino core if True then -u
        (sign of displacement is flipped) is applied.
        Default is False i.e. soft core is created.


    center : tuple of floats
        Coordinates of dislocation core (center) (x, y, z).
        Default is (0., 0., 0.)

    Returns
    -------
    ase.Atoms object
        Atoms object with predicted tetrahedral
        positions around dislocation core.

    """

    axes = np.array([[1, 1, -2],
                     [-1, 1, 0],
                     [1, 1, 1]])

    unit_cell = BodyCenteredCubic(directions=axes.tolist(),
                                  size=(1, 1, 1), symbol=symbol,
                                  pbc=(False, False, True),
                                  latticeconstant=alat)

    BCCTetras = BodyCenteredCubicTetrahedralFactory()

    impurities = BCCTetras(directions=axes.tolist(),
                           size=(1, 1, 1),
                           symbol=imp_symbol,
                           pbc=(False, False, True),
                           latticeconstant=alat)

    impurities = impurities[impurities.positions.T[2] < alat*1.2]
    impurities.set_cell(unit_cell.get_cell())
    impurities.wrap()

    disloCenterY = alat * np.sqrt(2.)/6.0
    disloCenterX = alat * np.sqrt(6.)/6.0

    impurities.positions[:, 0] -= disloCenterX
    impurities.positions[:, 1] -= disloCenterY

    # size of the cubic cell as a 112 direction
    Lx = int(round((scan_r)/(alat * np.sqrt(6.))))

    # size of the cubic cell as a 110 direction
    Ly = int(round((scan_r) / (alat * np.sqrt(2.))))
    # factor 2 to ,ake shure odd number of images is translated
    # it is important for the correct centering of the dislocation core
    bulk_tetra = impurities * (2*(Lx + 1), 2*(Ly + 1), 1)
    # make 0, 0, at the center

    # make 0, 0, at the center
    bulk_tetra.positions[:, 0] -= (Lx + 1) * alat * np.sqrt(6.) - center[0]
    bulk_tetra.positions[:, 1] -= (Ly + 1) * alat * np.sqrt(2.) - center[1]

    x, y, z = bulk_tetra.positions.T

    radius_x_y_zero = np.sqrt(x**2 + y**2)
    mask_zero = radius_x_y_zero < scan_r

    radius_x_y_center = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    mask_center = radius_x_y_center < scan_r

    final_mask = mask_center | mask_zero
    # leave only atoms inside the cylinder
    bulk_tetra = bulk_tetra[final_mask]

    # Create a Stroh ojbect with junk data
    stroh = am.defect.Stroh(am.ElasticConstants(C11=141, C12=110, C44=98),
                            np.array([0, 0, 1]))

    c = am.ElasticConstants(C11=C11, C12=C12, C44=C44)
    burgers = alat * np.array([1., 1., 1.])/2.

    # Solving a new problem with Stroh.solve
    stroh.solve(c, burgers, axes=axes)

    dislo_tetra = bulk_tetra.copy()

    impurities_u = stroh.displacement(bulk_tetra.positions - center)
    impurities_u = -impurities_u if hard_core else impurities_u

    dislo_tetra.positions += impurities_u

    return dislo_tetra


def screw_cyl_octahedral(alat, C11, C12, C44,
                         scan_r=15,
                         symbol="W",
                         imp_symbol='H',
                         hard_core=False,
                         center=(0., 0., 0.)):
    """Generates a set of octahedral positions with `scan_r` radius.
       Applies the screw dislocation displacement for creating an initial guess
       for the H positions at dislocation core.

    Parameters
    ----------
    alat : float
        Lattice constant of the material.
    C11 : float
        C11 elastic constant of the material.
    C12 : float
        C12 elastic constant of the material.
    C44 : float
        C44 elastic constant of the material.
    symbol : string
        Symbol of the element to pass to ase.lattuce.cubic.SimpleCubicFactory
        default is "W" for tungsten
    imp_symbol : string
        Symbol of the elemnt to pass creat Atoms object
        default is "H" for hydrogen
    symbol : string
        Symbol of the elemnt to pass creat Atoms object
    hard_core : float
        Type of the dislocatino core if True then -u
        (sign of displacement is flipped) is applied.
        Default is False i.e. soft core is created.
    center : tuple of floats
        Coordinates of dislocation core (center) (x, y, z).
        Default is (0., 0., 0.)

    Returns
    -------
    ase.Atoms object
        Atoms object with predicted tetrahedral
        positions around dislocation core.

    """
    # TODO: Make one function for impurities and pass factory to it:
    # TODO: i.e. octahedral or terahedral

    axes = np.array([[1, 1, -2],
                     [-1, 1, 0],
                     [1, 1, 1]])

    unit_cell = BodyCenteredCubic(directions=axes.tolist(),
                                  size=(1, 1, 1), symbol=symbol,
                                  pbc=(False, False, True),
                                  latticeconstant=alat)

    BCCOctas = BodyCenteredCubicOctahedralFactory()

    impurities = BCCOctas(directions=axes.tolist(),
                          size=(1, 1, 1), symbol=imp_symbol,
                          pbc=(False, False, True),
                          latticeconstant=alat)

    impurities = impurities[impurities.positions.T[2] < alat*1.2]
    impurities.set_cell(unit_cell.get_cell())
    impurities.wrap()

    disloCenterY = alat * np.sqrt(2.)/6.0
    disloCenterX = alat * np.sqrt(6.)/6.0

    impurities.positions[:, 0] -= disloCenterX
    impurities.positions[:, 1] -= disloCenterY

    L = int(round(2.0*scan_r/(alat*np.sqrt(2.)))) + 1

    bulk_octa = impurities * (L, L, 1)

    # make 0, 0, at the center
    bulk_octa.positions[:, 0] -= L * alat * np.sqrt(6.)/2. - center[0]
    bulk_octa.positions[:, 1] -= L * alat * np.sqrt(2.)/2. - center[1]

    x, y, z = bulk_octa.positions.T

    radius_x_y_zero = np.sqrt(x**2 + y**2)
    mask_zero = radius_x_y_zero < scan_r

    radius_x_y_center = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    mask_center = radius_x_y_center < scan_r

    final_mask = mask_center | mask_zero
    # leave only atoms inside the cylinder
    bulk_octa = bulk_octa[final_mask]

    # Create a Stroh ojbect with junk data
    stroh = am.defect.Stroh(am.ElasticConstants(C11=141, C12=110, C44=98),
                            np.array([0, 0, 1]))

    c = am.ElasticConstants(C11=C11, C12=C12, C44=C44)
    burgers = alat * np.array([1., 1., 1.])/2.

    # Solving a new problem with Stroh.solve
    stroh.solve(c, burgers, axes=axes)

    dislo_octa = bulk_octa.copy()

    impurities_u = stroh.displacement(bulk_octa.positions - center)
    impurities_u = -impurities_u if hard_core else impurities_u

    dislo_octa.positions += impurities_u

    return dislo_octa


class BodyCenteredCubicTetrahedralFactory(SimpleCubicFactory):
    """A factory for creating tetrahedral lattices in bcc structure"""
    xtal_name = "bcc_tetrahedral"

    bravais_basis = [[0.0, 0.5, 0.25],
                     [0.0, 0.5, 0.75],
                     [0.0, 0.25, 0.5],
                     [0.0, 0.75, 0.5],
                     [0.5, 0.0, 0.75],
                     [0.25, 0.0, 0.5],
                     [0.75, 0.0, 0.5],
                     [0.5, 0.0, 0.25],
                     [0.5, 0.25, 0.0],
                     [0.5, 0.75, 0.0],
                     [0.25, 0.5, 0.0],
                     [0.75, 0.5, 0.0]]


class BodyCenteredCubicOctahedralFactory(SimpleCubicFactory):
    """A factory for creating octahedral lattices in bcc structure"""
    xtal_name = "bcc_octahedral"

    bravais_basis = [[0.0, 0.0, 0.5],
                     [0.5, 0.0, 0.0],
                     [0.5, 0.0, 0.5],
                     [0.0, 0.5, 0.0],
                     [0.0, 0.5, 0.5],
                     [0.5, 0.5, 0.0]]


def dipole_displacement_angle(W_bulk, dislo_coord_left, dislo_coord_right,
                              shift=0.0, mode=1.0):
    """
        Generates a simple displacement field for two dislocations in a dipole
        configuration uding simple Voltera solution as u = b/2 * angle
    """


    burgers = W_bulk.cell[2][2]

    shifted_positions = W_bulk.positions + shift - dislo_coord_left
    x, y, __ = shifted_positions.T
    displacement_left = np.arctan2(y, x) * burgers / (2.0 * np.pi)

    shifted_positions = W_bulk.positions + shift - dislo_coord_right
    x, y, __ = shifted_positions.T
    displacement_right = np.arctan2(y, mode*x) * burgers / (2.0 * np.pi)

    # make two easy core configurations

    u_dipole = np.zeros_like(W_bulk.positions)
    u_dipole.T[2] = displacement_left - mode*displacement_right

    return u_dipole


def get_u_img(W_bulk,
              dislo_coord_left,
              dislo_coord_right,
              n_img=10, n1_shift=0, n2_shift=0):
    """
        Function for getting displacemnt filed for images of quadrupole cells
        used by `make_screw_quadrupole`
    """

    u_img = np.zeros_like(W_bulk.positions)

    C1_quadrupole, C2_quadrupole, __ = W_bulk.get_cell()

    for n1 in range(-n_img, n_img + 1):
        for n2 in range(-n_img, n_img + 1):

            shift = n1 * C1_quadrupole + n2 * C2_quadrupole

            if n1 != n1_shift or n2 != n2_shift:

                u_img += dipole_displacement_angle(W_bulk,
                                                   dislo_coord_left + shift,
                                                   dislo_coord_right + shift,
                                                   shift=n2_shift*C2_quadrupole + n1_shift*C1_quadrupole)

    return u_img


def make_screw_quadrupole(alat,
                          left_shift=0,
                          right_shift=0,
                          n1u=5,
                          symbol="W"):
    """Generates a screw dislocation dipole configuration
       for effective quadrupole arrangement. Works for BCC systems.

    Parameters
    ----------
    alat : float
        Lattice parameter of the system in Angstrom.
    left_shift : float, optional
        Shift of the left dislocation core in number of dsitances to next
        equivalent disocation core positions needed for creation for final
        configuration for NEB. Default is 0.
    right_shift : float, optional
        shift of the right dislocation core in number of dsitances to next
        equivalent disocation core positions needed for creation for final
        configuration for NEB. Default is 0.
    n1u : int, odd number
        odd number! length of the cell a doubled distance between core along x.
        Main parameter to calculate cell vectors
    symbol : string
        Symbol of the element to pass to ase.lattuce.cubic.SimpleCubicFactory
        default is "W" for tungsten

    Returns
    -------
    disloc_quadrupole : ase.Atoms
        Resulting quadrupole configuration.
    W_bulk : ase.Atoms
        Perfect system.
    dislo_coord_left : list of float
        Coodrinates of left dislocation core [x, y]
    dislo_coord_right : list of float
        Coodrinates of right dislocation core [x, y]

    Notes
    -----

    Calculation of cell vectors
    +++++++++++++++++++++++++++
    From [1]_ we take:

    - Unit vectors for the cell are:

    .. math::

        u = \frac{1}{3}[1 \bar{2} 1];

    .. math::

        v = \frac{1}{3}[2 \bar{1} \bar{1}];

    .. math::

        z = b = \frac{1}{2}[1 1 1];

    - Cell vectors are:

    .. math::

        C_1 = n^u_1 u + n^v_1 v + C^z_1 z;

    .. math::

        C_2 = n^u_2 u + n^v_2 v + C^z_2 z;

    .. math::

        C_3 = z

    - For quadrupole arrangement n1u needs to be odd number,
      for 135 atoms cell we take n1u=5

    - To have quadrupole as as close as possible to a square one has to take:
    .. math::

        2 n^u_2 + n^v_2 = n^u_1

    .. math::

        n^v_2 \approx \frac{n^u_1}{\sqrt{3}}

    - for n1u = 5:

    .. math::

        n^v_2 \approx \frac{n^u_1}{\sqrt{3}} = 2.89 \approx 3.0

    .. math::

        n^u_2 = \frac{1}{2} (n^u_1 - n^v_2) \approx \frac{1}{2} (5-3)=1

    - Following [2]_ cell geometry is optimized by ading tilt compomemts
    Cz1 and Cz2 for our case of n1u = 3n - 1:

    Easy core

    .. math::

        C^z_1 = + \frac{1}{3}

    .. math::

        C^z_2 = + \frac{1}{6}

    Hard core

    .. math::

        C^z_1 = + \frac{1}{3}

    .. math::

        C^z_2 = + \frac{1}{6}

    may be typo in the paper check the original!

    References:
    +++++++++++

    .. [1] Ventelon, L. & Willaime, F. J 'Core structure and Peierls potential
       of screw dislocations in alpha-Fe from first principles: cluster versus
       dipole approaches' Computer-Aided Mater Des (2007) 14(Suppl 1): 85.
       https://doi.org/10.1007/s10820-007-9064-y

    .. [2] Cai W. (2005) Modeling Dislocations Using a Periodic Cell.
       In: Yip S. (eds) Handbook of Materials Modeling. Springer, Dordrecht
       https://link.springer.com/chapter/10.1007/978-1-4020-3286-8_42

    """

    unit_cell = BodyCenteredCubic(directions=[[1, -2, 1],
                                      [2, -1, -1],
                                      [1, 1, 1]],
                                  symbol=symbol,
                                  pbc=(True, True, True),
                                  latticeconstant=alat, debug=0)

    unit_cell_u, unit_cell_v, unit_cell_z = unit_cell.get_cell()

    # calculate the cell vectors according to the Ventelon paper
    # the real configrution depends on rounding check it here

    n2v = int(np.rint(n1u/np.sqrt(3.0)))
    # when the n1u - n2v difference is odd it is impossible to have
    # perfect arrangemt of translation along x with C2 equal to 0.5*n1u
    # choice of rounding between np.ceil() and np.trunc() makes a different
    # configuration but of same quality of arrangement of quadrupoles (test)
    n2u = np.ceil((n1u - n2v) / 2.)
    n1v = 0

    print("Not rounded values of C2 componets: ")
    print("n2u: %.2f,  n2v: %.2f" % ((n1u - n2v) / 2., n1u/np.sqrt(3.0)))
    print("Calculated cell vectors from n1u = %i" % n1u)
    print("n1v = %i" % n1v)
    print("n2u = %i" % n2u)
    print("n2v = %i" % n2v)

    bulk = unit_cell.copy()*[n1u, n2v, 1]

    # add another periodic shift in x direction to c2 vector
    # for proper periodicity (n^u_2=1) of the effective quadrupole arrangement

    bulk.cell[1] += n2u * unit_cell_u

    C1_quadrupole, C2_quadrupole, C3_quadrupole = bulk.get_cell()

    # calulation of dislocation cores positions
    # distance between centers of triangles along x
    # move to odd/even number -> get to upward/downward triangle
    x_core_dist = alat * np.sqrt(6.)/6.0

    # distance between centers of triangles along y
    y_core_dist = alat * np.sqrt(2.)/6.0

    # separation of the cores in a 1ux1v cell
    nx_left = 2
    nx_right = 5

    if n2v % 2 == 0:  # check if the number of cells in y direction is even
        # Even: then introduce cores between two equal halfes of the cell
        ny_left = -2
        ny_right = -1

    else:  # Odd: introduce cores between two equal halfes of the cell
        ny_left = 4
        ny_right = 5

    nx_left += 2.0 * left_shift
    nx_right += 2.0 * right_shift

    dislo_coord_left = np.array([nx_left * x_core_dist,
                                 ny_left * y_core_dist,
                                0.0])

    dislo_coord_right = np.array([nx_right * x_core_dist,
                                  ny_right * y_core_dist,
                                  0.0])

    # caclulation of the shifts of the inital cores coordinates for the final
    # quadrupole arrangements

    # different x centering preferences for odd and even values
    if n2v % 2 == 0:  # check if the number of cells in y direction is even
        # Even:
        dislo_coord_left += (n2u - 1) * unit_cell_u
        dislo_coord_right += (n2u - 1 + np.trunc(n1u/2.0)) * unit_cell_u

    else:  # Odd:
        dislo_coord_left += n2u * unit_cell_u
        dislo_coord_right += (n2u + np.trunc(n1u/2.0)) * unit_cell_u

    dislo_coord_left += np.trunc(n2v/2.0) * unit_cell_v
    dislo_coord_right += np.trunc(n2v/2.0) * unit_cell_v

    u_quadrupole = dipole_displacement_angle(bulk,
                                             dislo_coord_left,
                                             dislo_coord_right)

    # get the image contribution from the dipoles around
    # (default value of N images to scan n_img=10)
    u_img = get_u_img(bulk,
                      dislo_coord_left,
                      dislo_coord_right)

    u_sum = u_quadrupole + u_img

    # calculate the field of neghbouring cell to estimate
    # linear u_err along C1 and C2 (see. Cai paper)

    # u_err along C2

    n1_shift = 0
    n2_shift = 1

    shift = n1_shift*C1_quadrupole + n2_shift*C2_quadrupole

    u_quadrupole_shifted = dipole_displacement_angle(bulk,
                                                     dislo_coord_left + shift,
                                                     dislo_coord_right + shift,
                                                     shift=shift)

    u_img_shifted = get_u_img(bulk,
                              dislo_coord_left,
                              dislo_coord_right,
                              n1_shift=n1_shift, n2_shift=n2_shift)

    u_sum_shifted = u_quadrupole_shifted + u_img_shifted

    delta_u = u_sum - u_sum_shifted

    delta_u_C2 = delta_u.T[2].mean()
    print("delta u c2: %.2f " % delta_u_C2)

    # u_err along C1

    n1_shift = 1
    n2_shift = 0

    shift = n1_shift*C1_quadrupole + n2_shift*C2_quadrupole

    u_quadrupole_shifted = dipole_displacement_angle(bulk,
                                                     dislo_coord_left + shift,
                                                     dislo_coord_right + shift,
                                                     shift=shift)

    u_img_shifted = get_u_img(bulk,
                              dislo_coord_left,
                              dislo_coord_right,
                              n1_shift=n1_shift, n2_shift=n2_shift)

    u_sum_shifted = u_quadrupole_shifted + u_img_shifted

    delta_u = u_sum - u_sum_shifted

    delta_u_C1 = delta_u.T[2].mean()
    print("delta u c1: %.3f" % delta_u_C1)

    x_scaled, y_scaled, __ = bulk.get_scaled_positions(wrap=False).T

    u_err_C2 = (y_scaled - 0.5)*delta_u_C2

    u_err_C1 = delta_u_C1*(x_scaled - 0.5)

    u_err = u_err_C1 + u_err_C2

    # Calculate the u_tilt to accomodate the stress (see. Cai paper)

    burgers = bulk.cell[2][2]

    u_tilt = 0.5 * burgers * (y_scaled - 0.5)

    final_u = u_sum
    final_u.T[2] += u_err - u_tilt

    disloc_quadrupole = bulk.copy()
    disloc_quadrupole.positions += final_u
    # tilt the cell according to the u_tilt
    disloc_quadrupole.cell[1][2] -= burgers/2.0
    bulk.cell[1][2] -= burgers/2.0

    return disloc_quadrupole, bulk, dislo_coord_left, dislo_coord_right


def make_edge_cyl_001_100(a0, C11, C12, C44,
                          cylinder_r,
                          cutoff=5.5,
                          tol=1e-6,
                          symbol="W"):
    """Function to produce consistent edge dislocation configuration.

    Parameters
    ----------
    alat : float
        Lattice constant of the material.
    C11 : float
        C11 elastic constant of the material.
    C12 : float
        C12 elastic constant of the material.
    C44 : float
        C44 elastic constant of the material.
    cylinder_r : float
        Radius of cylinder of unconstrained atoms around the
        dislocation  in angstrom.
    cutoff : float
        Potential cutoff for determenition of size of
        fixed atoms region (2*cutoff)
    tol : float
        Tolerance for generation of self consistent solution.
    symbol : string
        Symbol of the element to pass to ase.lattuce.cubic.SimpleCubicFactory
        default is "W" for tungsten

    Returns
    -------
    bulk : ase.Atoms object
        Bulk configuration.
    disloc : ase.Atoms object
        Dislocation configuration.
    disp : np.array
        Correstonding displacement.
    """

    # Create a Stroh ojbect with junk data
    stroh = am.defect.Stroh(am.ElasticConstants(C11=141, C12=110, C44=98),
                            np.array([0, 0, 1]))

    axes = np.array([[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]])

    c = am.ElasticConstants(C11=C11, C12=C12, C44=C44)
    burgers = a0 * np.array([1., 0., 0.])

    # Solving a new problem with Stroh.solve
    # Does not work with the new version of atomman
    stroh.solve(c, burgers, axes=axes)

    unit_cell = BodyCenteredCubic(directions=axes.tolist(),
                                  size=(1, 1, 1), symbol=symbol,
                                  pbc=(False, False, True),
                                  latticeconstant=a0)

    bulk = unit_cell.copy()

    # shift to make the zeros of the cell betweem the atomic planes
    # and under the midplane on Y axes
    X_midplane_shift = -0.25*a0
    Y_midplane_shift = -0.25*a0

    bulk_shift = [X_midplane_shift,
                  Y_midplane_shift,
                  0.0]

    bulk.positions += bulk_shift

    tot_r = cylinder_r + 2*cutoff + 0.01

    Lx = int(round(tot_r/a0))
    Ly = int(round(tot_r/a0))

    # factor 2 to make sure odd number of images is translated
    # it is important for the correct centering of the dislocation core
    bulk = bulk * (2*Lx, 2*Ly, 1)

    center_shift = [Lx * a0, Ly * a0, 0.0]

    bulk.positions -= center_shift
    # bulk.write("before.xyz")

    disp1 = stroh.displacement(bulk.positions)
    disloc = bulk.copy()
    res = np.inf
    i = 0
    while res > tol:
        disloc.positions = bulk.positions + disp1
        disp2 = stroh.displacement(disloc.positions)
        res = np.abs(disp1 - disp2).max()
        disp1 = disp2
        print 'disloc SCF', i, '|d1-d2|_inf =', res
        i += 1
        if i > 10:
            raise RuntimeError('Self-consistency did \
                                not converge in 10 cycles')
    disp = disp2

    x, y, z = disloc.positions.T
    radius_x_y_zero = np.sqrt(x**2 + y**2)
    mask = radius_x_y_zero < tot_r
    disloc = disloc[mask]
    bulk = bulk[mask]
    # disloc.write("after_disp.xyz")

    x, y, z = disloc.positions.T
    radius_x_y_zero = np.sqrt(x**2 + y**2)
    mask_zero = radius_x_y_zero > cylinder_r
    fix_atoms = FixAtoms(mask=mask_zero)
    disloc.set_constraint(fix_atoms)

    return bulk, disloc, disp
