"""
An example for how to make use of:
(i) the file_path to defect entry function
(i) all plotting functionalities with PyCDT
"""
from pycdt.utils.parse_calculations import SingleDefectParser
from pycdt.utils.plotter import SingleParticlePlotter, StructureRelaxPlotter
from pycdt.corrections.correction_plotting import KumagaiPlotter, FreysoldtPlotter
from monty.serialization import loadfn, dumpfn
from monty.json import jsanitize

"""THESE FOUR THINGS ARE TO BE MODIFIED"""
# defect_path = "/global/cscratch1/sd/dbroberg/launchers/block_2018-11-09-16-14-36-067309/launcher_2019-01-30-19-23-31-202707"
# bulk_path = "/global/cscratch1/sd/dbroberg/launchers/block_2018-10-04-00-47-58-491296/launcher_2018-10-19-21-08-32-888077"
defect_path = "/Users/dpbroberg/Documents/research/research_codes/testing/testing_pycdt_bug_shivani/TiPbO3_defect/vac_3_O/charge_0"
bulk_path = "/Users/dpbroberg/Documents/research/research_codes/testing/testing_pycdt_bug_shivani/TiPbO3_defect/bulk"
dielectric = [12.08, 12.08, 10.28]
defect_charge = 0
mpid = None #dont have to set this, but you can if you want
""""""

parse_defect = True

if parse_defect:
    sdp = SingleDefectParser( defect_path, bulk_path, dielectric, defect_charge=defect_charge, mpid=mpid)
    defect_entry = sdp.get_defect_entry(run_compatibility=True)
    for skey in ["initial_defect_structure", "final_defect_structure", 'bulk_sc_structure']:
        defect_entry.parameters[skey] = defect_entry.parameters[skey].as_dict()
    defect_entry_dict = jsanitize( defect_entry.as_dict())
    dumpfn( defect_entry_dict, 'defect_object.json')
else:
    print("Skipping parsing and loading from json...")
    defect_entry = loadfn( 'defect_object.json')
    for skey in ["initial_defect_structure", "final_defect_structure", 'bulk_sc_structure']:
        defect_entry.parameters[skey].from_dict( defect_entry.parameters[skey])


"""NOW do a whole bunch of useful plotting"""
# plot Freysoldt plots
print("Parsing Freysoldt plot")
fm = defect_entry.parameters['freysoldt_meta']
print_out = ['freysoldt_potalign', 'freysoldt_electrostatic', 'freysoldt_potential_alignment_correction',
             'pot_corr_uncertainty_md']
for k in print_out:
    print("{} = {}\n".format(k, fm[k]))

ppd = fm['pot_plot_data']
for ax, ax_dict in ppd.items():
    print('Axis = {}'.format(ax))
    fp = FreysoldtPlotter.from_dict( ax_dict)
    p = fp.plot(title="axis "+str(ax))
    p.savefig("FreysoldtPotentialAlignment_ax{}.pdf".format( str(ax)))

# plot Kuamgai plots
print("Parsing Kumagai plot")
km = defect_entry.parameters['kumagai_meta']
print_out = ['gamma', 'sampling_radius', 'kumagai_potalign', 'kumagai_electrostatic',
             'kumagai_potential_alignment_correction', 'pot_corr_uncertainty_md']
for k in print_out:
    print("{} = {}\n".format(k, km[k]))

ppd = km['pot_plot_data']

kp = KumagaiPlotter.from_dict({'site_dict': ppd, "sampling_radius": km['sampling_radius'],
                               'potalign': km['kumagai_potalign']})
p = kp.plot()
p.savefig("KumagaiPotentialAlignment.pdf")


#Plot wavefunction plots
spp = SingleParticlePlotter( defect_entry.parameters["defect_ks_delocal_data"])
if len(spp.localized_bands):
    for lb_ind in spp.localized_bands:
        p = spp.plot( lb_ind, title="Band index {}".format( lb_ind))
        p.savefig("BandPlot{}.pdf".format( str(lb_ind)))
        print('\tPlotted {}'.format(lb_ind))
else:
    print("No plotting to be done...")


#Plot structural relaxation plots
srp = StructureRelaxPlotter( defect_entry.parameters['delocalization_meta']['structure_relax']['metadata']['full_structure_relax_data'],
                             defect_entry.parameters["kumagai_meta"]['sampling_radius'])
p = srp.plot()
p.savefig("StructureRelaxation.pdf")
print('Plotted Structural Relaxation')
