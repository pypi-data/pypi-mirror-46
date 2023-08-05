#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Project "Sensitivity Analysis of Rule-Based Models", Rodrigo Santibáñez, 2019
To be used with KaSim. Please refer to other subprojects for other stochastic simulators support
Citation:
'''

__author__  = 'Rodrigo Santibáñez'
__license__ = 'gpl-3.0'
__software__ = 'kasim-v4.0'

import argparse, glob, multiprocessing, os, re, shutil, subprocess, sys, time
import pandas, numpy, seaborn
import matplotlib.pyplot as plt
from SALib.sample import saltelli
from SALib.analyze import sobol

def safe_checks():
	error_msg = ''
	if shutil.which(opts['python']) is None:
		error_msg += 'python3 (at {:s}) can\'t be called to perform error calculation.\n' \
			'You could use --python {:s}\n'.format(opts['python'], shutil.which('python3'))

	# check for simulators
	#if shutil.which(opts['bng2']) is None:
		#error_msg += 'BNG2 (at {:s}) can\'t be called to perform simulations.\n' \
			#'Check the path to BNG2.'.format(opts['bng2'])
	if shutil.which(opts['kasim']) is None:
		error_msg += 'KaSim (at {:s}) can\'t be called to perform simulations.\n' \
			'Check the path to KaSim.'.format(opts['kasim'])
	#if shutil.which(opts['nfsim']) is None:
		#error_msg += 'NFsim (at {:s}) can\'t be called to perform simulations.\n' \
			#'Check the path to NFsim.'.format(opts['nfsim'])
	#if shutil.which(opts['piskas']) is None:
		#error_msg += 'PISKaS (at {:s}) can\'t be called to perform simulations.\n' \
			#'Check the path to PISKaS.'.format(opts['piskas'])

	# check for slurm
	if opts['slurm'] is not None or opts['slurm'] == '':
		if not sys.platform.startswith('linux'):
			error_msg += 'SLURM do not support WindowsOS and macOS (https://slurm.schedmd.com/platforms.html)\n'
		else:
			if shutil.which('sinfo') is None:
				error_msg += 'You specified a SLURM partition but SLURM isn\'t installed on your system.\n' \
					'Delete --slurm to use the python multiprocessing API or install SLURM (https://pleione.readthedocs.io/en/latest/SLURM.html)\n'
			else:
				cmd = 'sinfo -hp {:s}'.format(opts['slurm'])
				cmd = re.findall(r'(?:[^\s,"]|"+(?:=|\\.|[^"])*"+)+', cmd)
				out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
				if out == b'':
					error_msg += 'You specified an invalid SLURM partition.\n' \
						'Please, use --slurm $SLURM_JOB_PARTITION or delete --slurm to use the python multiprocessing API.\n'

	# check if model file exists
	if not os.path.isfile(opts['model']):
		error_msg += 'The "{:s}" file cannot be opened.\n' \
			'Please, check the path to the model file.\n'.format(opts['model'])

	# print error
	if error_msg != '':
		print(error_msg)
		raise ValueError(error_msg)

	return 0

def parallelize(cmd):
	proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
	out, err = proc.communicate()
	proc.wait()
	return 0

def argsparser():
	parser = argparse.ArgumentParser(description = 'Perform a sensitivity analysis of RBM parameters employing the Morris sequence.')

	# required arguments
	parser.add_argument('--model'  , metavar = 'str'  , type = str  , required = True , default = 'model.kappa'   , help = 'RBM with tagged variables to analyze')
	parser.add_argument('--final'  , metavar = 'float', type = str  , required = True , default = '100'           , help = 'limit time to simulate')
	parser.add_argument('--steps'  , metavar = 'float', type = str  , required = True , default = '1'             , help = 'time interval to simulate')
	# choose one or more evaluation functions

	# useful paths
	#parser.add_argument('--bng2'   , metavar = 'path' , type = str  , required = False, default = '~/bin/bng2'    , help = 'BioNetGen path, default ~/bin/bng2')
	parser.add_argument('--kasim'  , metavar = 'path' , type = str  , required = False, default = '~/bin/kasim4'  , help = 'KaSim path, default ~/bin/kasim4')
	#parser.add_argument('--nfsim'  , metavar = 'path' , type = str  , required = False, default = '~/bin/nfsim'   , help = 'NFsim path, default ~/bin/nfsim')
	#parser.add_argument('--piskas' , metavar = 'path' , type = str  , required = False, default = '~/bin/piskas'  , help = 'PISKaS path, default ~/bin/piskas')
	parser.add_argument('--python' , metavar = 'path' , type = str  , required = False, default = '~/bin/python3' , help = 'python path, default ~/bin/python3')

	# distribute computation with SLURM, otherwise with python multiprocessing API
	parser.add_argument('--slurm'  , metavar = 'str'  , type = str  , required = False, default = None            , help = 'SLURM partition to use, default None')

	# general options
	parser.add_argument('--type'   , metavar = 'str'  , type = str  , required = False, default = 'global'        , help = 'global or local sensitivity analysis')
	parser.add_argument('--tick'   , metavar = 'int'  , type = str  , required = False, default = '0'             , help = 'local sensitivity ...')
	parser.add_argument('--size'   , metavar = 'int'  , type = str  , required = False, default = '1'             , help = 'local sensitivity ...')
	parser.add_argument('--beat'   , metavar = 'float', type = str  , required = False, default = '0.3'           , help = 'local sensitivity time step to calculate DIN')
	# more general options
	parser.add_argument('--tmin'   , metavar = 'float', type = str  , required = False, default = '0'             , help = 'Initial time to calculate the Dynamical Influence Network')
	parser.add_argument('--tmax'   , metavar = 'float', type = str  , required = False, default = None            , help = 'Final time to calculate the Dynamical Influence Network')
	parser.add_argument('--prec'   , metavar = 'str'  , type = str  , required = False, default = '7g'            , help = 'precision and format of parameter values, default 7g')
	parser.add_argument('--grid'   , metavar = 'int'  , type = str  , required = False, default = '10'            , help = 'number of samples N * (2D + 2), default N = 10, D = number of parameters')

	# other options
	parser.add_argument('--syntax' , metavar = 'str'  , type = str  , required = False, default = '4'             , help = 'KaSim syntax, default 4')
	parser.add_argument('--binary' , metavar = 'str'  , type = str  , required = False, default = 'model'         , help = 'KaSim binary prefix, default model')
	parser.add_argument('--results', metavar = 'str'  , type = str  , required = False, default = 'results'       , help = 'output folder where to move the results, default results')
	parser.add_argument('--samples', metavar = 'str'  , type = str  , required = False, default = 'samples'       , help = 'folder to save the generated models, default samples')
	parser.add_argument('--rawdata', metavar = 'str'  , type = str  , required = False, default = 'simulations'   , help = 'folder to save the simulations, default simulations')
	parser.add_argument('--figures', metavar = 'str'  , type = str  , required = False, default = 'figures'       , help = 'folder to save the figures in eps, default figures')
	parser.add_argument('--reports', metavar = 'str'  , type = str  , required = False, default = 'reports'       , help = 'folder to save the calculated sensitivity, default reports')

	args = parser.parse_args()

	if args.tmax is None:
		args.tmax = args.final

	return args

def ga_opts():
	return {
		# user defined options
		'model'     : args.model,
		'final'     : args.final, # not bng2
		'steps'     : args.steps, # not bng2
		#'bng2'      : os.path.expanduser(args.bng2), # bng2, nfsim only
		'kasim'     : os.path.expanduser(args.kasim), # kasim4 only
		#'piskas'    : os.path.expanduser(args.piskas), # piskas only
		#'nfsim'     : os.path.expanduser(args.nfsim), # nfsim only
		'python'    : os.path.expanduser(args.python),
		'slurm'     : args.slurm,
		'p_levels'  : int(args.grid),
		'type'      : args.type,
		'size'      : args.size,
		'tick'      : args.tick,
		'beat'      : args.beat,
		'tmin'      : args.tmin,
		'tmax'      : args.tmax,
		'par_prec'  : args.prec,
		'syntax'    : args.syntax, # kasim4 only
		#'binary'    : args.binary, # kasim4 beta only
		#'equil'     : args.equil, # nfsim only
		#'sync'      : args.sync, # piskas only
		'results'   : args.results,
		'samples'   : args.samples,
		'rawdata'   : args.rawdata,
		'figures'   : args.figures,
		'reports'   : args.reports,
		# non-user defined options
		'home'      : os.getcwd(),
		'null'      : '/dev/null',
		'max_error' : numpy.nan,
		#'bin_file'  : args.model[0].split('.')[0] + '.bin', # kasim4 beta only
		'systime'   : str(time.time()).split('.')[0],
		# useful data
		#'num_pars'  : 0,
		'par_name'  : [],
		}

def configurate():
	# read the model
	data = []
	with open(opts['model'], 'r') as infile:
		for line in infile:
			data.append(line)

	# find variables to analyze
	regex = '%\w+: \'(\w+)\' ' \
		'([-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?)\s+(?:\/\/|#)\s+' \
		'(\w+)\[([-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?)\s+' \
		'([-+]?(?:(?:\d*\.\d+)|(?:\d+\.?))(?:[Ee][+-]?\d+)?)\]\n'

	#num_pars = 0
	parameters = {}

	for line in range(len(data)):
		matched = re.match(regex, data[line])
		if matched:
			parameters[line] = [
				'par',
				matched.group(1), # parameter name
				matched.group(2), # original value
				matched.group(3), # sensitivity keyword
				matched.group(4), # lower bound
				matched.group(5), # upper bound
				]
			opts['par_name'].append(matched.group(1))
		else:
			parameters[line] = data[line]

	if len(opts['par_name']) == 0:
		error_msg = 'No variables to analyze.\n' \
			'Check if selected variables follow the regex (See Manual).'
		print(error_msg)
		raise ValueError(error_msg)

	return parameters

def populate():
	# 'parameters' dictionary stores everything in the model, particularly the parameters to analyze
	par_keys = list(parameters.keys())

	problem = {
		'names': opts['par_name'],
		'num_vars': len(opts['par_name']),
		'bounds': [],
		}

	for line in range(len(par_keys)):
		if parameters[line][0] == 'par':
			lower = float(parameters[par_keys[line]][4])
			upper = float(parameters[par_keys[line]][5])

			problem['bounds'].append([lower, upper])

	models = saltelli.sample(problem, int(opts['p_levels']))

	population = {}
	model_string = 'level{:0' + str(len(str(len(models)))) + 'd}'

	for model_index, model in enumerate(models):
		model_key = model_string.format(model_index+1)
		population[model_key, 'model'] = model_key
		for par_index, par_name in enumerate(opts['par_name']):
			population[model_key, par_name] = models[model_index][par_index]

	# add models sampling to population
	population['problem', 'definition'] = problem

	return population

def simulate():
	job_desc = {
		'nodes'     : 1,
		'ntasks'    : 1,
		'ncpus'     : 1,
		'null'      : opts['null'],
		'partition' : opts['slurm'],
		'job_name'  : 'child_{:s}'.format(opts['systime']),
		'stdout'    : 'stdout_{:s}.txt'.format(opts['systime']),
		'stderr'    : 'stderr_{:s}.txt'.format(opts['systime']),
		}

	# generate a kappa file per model
	par_keys = list(parameters.keys())
	par_string = '%var: \'{:s}\' {:.' + opts['par_prec'] + '}\n'

	for model in sorted(population.keys()):
		if model[1] == 'model':
			model_key = model[0]
			model_name = population[model_key, 'model']

			if opts['type'] == 'global':
				if opts['syntax'] == '4':
					flux = '%mod: [T] > {:s} do $DIN \"flux_{:s}.json\" [true];'.format(opts['tmin'], model_key) + \
						'%mod: [T] > {:s} do $DIN \"flux_{:s}.json\" [false];'.format(opts['tmax'], model_key)
				else: # kappa3.5 uses $FLUX instead of $DIN
					flux = '%mod: [T] > {:s} do $FLUX \"flux_{:s}.json\" [true]\n'.format(opts['tmin'], model_key) + \
						'%mod: [T] > {:s} do $FLUX \"flux_{:s}.json\" [false]'.format(opts['tmax'], model_key)
			else: # local sensitivity analysis
				if opts['syntax'] == '4':
					flux = '%mod: repeat (([T] > DIM_clock) && (DIM_tick > (DIM_length - 1))) do $DIN "flux_".(DIM_tick - DIM_length).".json" [false] until [false];'
				else: # kappa3.5 uses $FLUX instead of $DIN
					flux = '\n# Added to calculate a local sensitivity analysis\n' + \
						'%var: \'DIN_beat\' {:s}\n'.format(opts['beat']) + \
						'%var: \'DIN_length\' {:s}\n'.format(opts['size']) + \
						'%var: \'DIN_tick\' {:s}\n'.format(opts['tick']) + \
						'%var: \'DIN_clock\' {:s}\n'.format(opts['tmin']) + \
						'%mod: repeat (([T] > DIN_clock) && (DIN_tick > (DIN_length - 1))) do ' + \
							'$FLUX \"flux_{:s}\".(DIN_tick - DIN_length).\".json\" [false] until [false]\n'.format(model_key) + \
						'%mod: repeat ([T] > DIN_clock) do ' + \
							'$FLUX "flux_{:s}".DIN_tick.".json" "probability" [true] until ((((DIN_tick + DIN_length) + 1) * DIN_beat) > [Tmax])\n'.format(model_key) + \
						'%mod: repeat ([T] > DIN_clock) do $UPDATE DIN_clock (DIN_clock + DIN_beat); $UPDATE DIN_tick (DIN_tick + 1) until [false]'

			model_path = './model_' + model_name + '.kappa'
			if not os.path.exists(model_path):
				with open(model_path, 'w') as file:
					for line in par_keys:
						if parameters[line][0] == 'par':
							file.write(par_string.format(parameters[line][1], population[model_key, parameters[line][1]]))
						else:
							file.write(parameters[line])
					# add the DIN perturbation at the end of the kappa file
					file.write(flux)

	# submit simulations to the queue
	squeue = []
	samples = opts['p_levels'] * (2 * len(opts['par_name']) + 2) # we are using saltelli sampling

	for model in sorted(population.keys()):
		if model[1] == 'model':
			model_key = model[0]
			model_name = population[model_key, 'model']
			output = 'model_{:s}.out.txt'.format(model_name)

			if not os.path.exists(output):
				job_desc['exec_kasim'] = '{:s} -i model_{:s}.kappa -l {:s} -p {:s} -o {:s} -syntax {:s} --no-log'.format( \
					opts['kasim'], model_name, opts['final'], opts['steps'], output, opts['syntax'])

				# use SLURM Workload Manager
				if opts['slurm'] is not None:
					cmd = os.path.expanduser('sbatch --no-requeue -p {partition} -N {nodes} -c {ncpus} -n {ntasks} -o {null} -e {null} -J {job_name} \
						--wrap ""{exec_kasim}""'.format(**job_desc))
					cmd = re.findall(r'(?:[^\s,"]|"+(?:=|\\.|[^"])*"+)+', cmd)
					out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
					while err == sbatch_error:
						out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
					squeue.append(out.decode('utf-8')[20:-1])

				# use multiprocessing.Pool
				else:
					cmd = os.path.expanduser(job_desc['exec_kasim'])
					cmd = re.findall(r'(?:[^\s,"]|"+(?:=|\\.|[^"])*"+)+', cmd)
					squeue.append(cmd)

	# check if squeued jobs have finished
	if opts['slurm'] is not None:
		for job_id in range(len(squeue)):
			cmd = 'squeue --noheader -j{:s}'.format(squeue[job_id])
			cmd = re.findall(r'(?:[^\s,"]|"+(?:=|\\.|[^"])*"+)+', cmd)
			out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
			while out.count(b'child') > 0 or err == squeue_error:
				time.sleep(1)
				out, err = subprocess.Popen(cmd, shell = False, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()

	#simulate with multiprocessing.Pool
	else:
		with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
			pool.map(parallelize, sorted(squeue), chunksize = 1)

	return population

def evaluate():
	sensitivity = {
		'din_hits' : {},
		'din_fluxes' : {},
		}

	din_hits = [] # list of column vector, one value per rule
	din_fluxes = [] # list of squeare numpy arrays, not symmetric
	files = sorted(glob.glob('./flux*json'))

	for fluxes in files:
		with open(fluxes, 'r') as file:
			data = pandas.read_json(file)
		din_hits.append(data['din_hits'].iloc[1:].values) # vector column of values
		tmp = [x for x in data['din_fluxs']] # vector column of list of values
		din_fluxes.append(pandas.DataFrame(tmp).values)

	# DIN hits are easy to evaluate recursively
	din_hits = pandas.DataFrame(data = din_hits)
	for rule in din_hits.columns:
		sensitivity['din_hits'][rule] = sobol.analyze(population['problem', 'definition'], din_hits[rule].values, print_to_console = False)

	# DIN fluxes are not that easy to evaluate recursively; data needs to be reshaped
	a, b = numpy.shape(din_fluxes[0][1:,1:])
	din_fluxes = pandas.DataFrame(data = [x[0] for x in [numpy.reshape(x[1:,1:], (1, a*b)) for x in din_fluxes]])
	for rule in din_fluxes.columns:
		sensitivity['din_fluxes'][rule] = sobol.analyze(population['problem', 'definition'], din_fluxes[rule].values, print_to_console = False)

	return sensitivity

def ranking():
	# get rule names from one DIN file
	files = sorted(glob.glob('./flux*json'))
	with open(files[0], 'r') as file:
		lst = pandas.read_json(file)

	reports = {
		'DINhits' : {},
		'DINfluxes' : {},
		}

	# DIN hits
	# reorder sensitivities for DIN hits
	x = sensitivity['din_hits']
	for key in ['S1', 'S1_conf', 'ST', 'ST_conf']:
		reports['DINhits'][key] = pandas.DataFrame([x[k][key] for k in x.keys()],
			columns = opts['par_name'], index = lst['din_rules'][1:]).rename_axis('rules')

		with open(f'./report_DINhits_{key}.txt', 'w') as file:
			reports['DINhits'][key].to_csv(file, sep = '\t')

		# plot sensitivities and half of the 95% confidence interval, separately
		for rule in reports['DINhits'][key].index:
			fig, ax = plt.subplots(1, 1, figsize = (4, 3), dpi = 100)
			seaborn.barplot(y = reports['DINhits'][key].columns, x = reports['DINhits'][key].loc[rule, :], ax = ax) # horizontal barplot (x -> y)

			seaborn.despine()
			plt.tight_layout()
			fig.savefig(f'./figure_DINhits_{key}_over_{rule}.eps', format = 'eps', bbox_inches = 'tight', dpi = 300)
			plt.close()

	# plot sensitivities with 95% confidence interval, together
	for key in ['S1', 'ST']:
		for rule in reports['DINhits'][key].index:
			fig, ax = plt.subplots(1, 1, figsize = (4, 3), dpi = 100)
			seaborn.barplot(y = reports['DINhits'][key].columns, x = reports['DINhits'][key].loc[rule, :], ax = ax,
				**{ 'xerr' : reports['DINhits'][key + '_conf'].loc[rule, :] }) # add the confidence interval to the horizontal barplot

			seaborn.despine()
			plt.tight_layout()
			fig.savefig(f'./figure_DINhits_{key}+95%_over_{rule}.eps', format = 'eps', bbox_inches = 'tight', dpi = 300)
			plt.close()

	for key in ['S2', 'S2_conf']:
		tmp = [pandas.DataFrame(x[k][key], columns = opts['par_name'], index = opts['par_name']).stack() for k in x.keys()]
		reports['DINhits'][key] = pandas.DataFrame(tmp, index = lst['din_rules'][1:]).rename_axis('rules')

		with open(f'./report_DINhits_{key}.txt', 'w') as file:
			reports['DINhits'][key].to_csv(file, sep = '\t')

	# plot second order sensitivities.
	# TODO
	# use a heatmap?

	# DIN fluxes
	# reorder sensitivities for DIN fluxes
	x = sensitivity['din_fluxes']
	# name index: parameter sensitivities over the influence of a 1st rule over a 2nd rule
	rules_names = list(lst['din_rules'][1:])
	first = [y for x in [[x]*len(rules_names) for x in rules_names] for y in x]
	second = rules_names * len(rules_names)

	for key in ['S1', 'S1_conf', 'ST', 'ST_conf']:
		reports['DINfluxes'][key] = pandas.DataFrame([x[k][key] for k in x.keys()], columns = opts['par_name']).fillna(0)
		reports['DINfluxes'][key]['1st'] = first
		reports['DINfluxes'][key]['2nd'] = second
		reports['DINfluxes'][key].set_index(['1st', '2nd'], inplace = True)

		with open(f'./report_DINfluxes_{key}.txt', 'w') as file:
			reports['DINfluxes'][key].to_csv(file, sep = '\t')

		# plot sensitivities and half of the 95% confidence interval, separately
		for rule_1st in reports['DINfluxes'][key].index.levels[0]:
			for rule_2nd in reports['DINfluxes'][key].index.levels[1]:
				fig, ax = plt.subplots(1, 1, figsize = (4, 3), dpi = 100)
				seaborn.barplot(y = reports['DINfluxes'][key].columns, x = reports['DINfluxes'][key].loc[rule_1st].loc[rule_2nd, :], ax = ax) # horizontal barplot (x -> y)

				if rule_1st == rule_2nd:
					ax.set_xlabel(f'Influence {rule_1st} over itself')
				else:
					ax.set_xlabel(f'Influence {rule_1st} over {rule_2nd}')

				seaborn.despine()
				plt.tight_layout()
				fig.savefig(f'./figure_DINfluxes_{key}_over_{rule_1st}_vs_{rule_2nd}.eps', format = 'eps', bbox_inches = 'tight', dpi = 300)
				plt.close()

	# plot sensitivities with 95% confidence interval, together
	for key in ['S1', 'ST']:
		for rule_1st in reports['DINfluxes'][key].index.levels[0]:
			for rule_2nd in reports['DINfluxes'][key].index.levels[1]:
				fig, ax = plt.subplots(1, 1, figsize = (4, 3), dpi = 100)
				seaborn.barplot(y = reports['DINfluxes'][key].columns, x = reports['DINfluxes'][key].loc[rule_1st].loc[rule_2nd, :], ax = ax,
					**{ 'xerr' : reports['DINfluxes'][key + '_conf'].loc[rule_1st].loc[rule_2nd, :] }) # add the confidence interval to the horizontal barplot

				if rule_1st == rule_2nd:
					ax.set_xlabel(f'Influence {rule_1st} over itself')
				else:
					ax.set_xlabel(f'Influence {rule_1st} over {rule_2nd}')

				seaborn.despine()
				plt.tight_layout()
				fig.savefig(f'./figure_DINfluxes_{key}+95%_over_{rule_1st}_vs_{rule_2nd}.eps', format = 'eps', bbox_inches = 'tight', dpi = 300)
				plt.close()

	for key in ['S2', 'S2_conf']:
		tmp = [pandas.DataFrame(x[k][key], columns = opts['par_name'], index = opts['par_name']).stack() for k in x.keys()]
		reports['DINfluxes'][key] = pandas.DataFrame(tmp).fillna(0)
		reports['DINfluxes'][key]['1st'] = first
		reports['DINfluxes'][key]['2nd'] = second
		reports['DINfluxes'][key].set_index(['1st', '2nd'], inplace = True)

		with open(f'./report_DINfluxes_{key}.txt', 'w') as file:
			reports['DINfluxes'][key].to_csv(file, sep = '\t')

	# plot second order sensitivities.
	# TODO
	# use a heatmap?

	return sensitivity

def clean():
	filelist = []
	fileregex = [
		'*.eps',      # figures
		'flux*.json', # DIN files
		'log*.txt',   # log file
		'*.kappa',    # kasim model files.
		'model*.txt', # kasim simulation outputs.
	]

	for regex in fileregex:
		filelist.append(glob.glob(regex))
	filelist = [ item for sublist in filelist for item in sublist ]

	for filename in filelist:
		if filename not in [ opts['model'] ]:
			os.remove(filename)

	return 0

def backup():
	results = opts['results'] + '_' + opts['systime']
	folders = {
		'samples' : results + '/' + opts['samples'],
		'rawdata' : results + '/' + opts['rawdata'],
		'figures' : results + '/' + opts['figures'],
		'reports' : results + '/' + opts['reports'],
	}

	# make backup folders
	os.mkdir(results)
	for folder in folders.values():
		os.mkdir(folder)

	# archive model files
	filelist = glob.glob('model_*.kappa')
	for filename in filelist:
		shutil.move(filename, folders['samples'])

	# archive fluxes outputs and simulations
	filelist = glob.glob('flux_*.json')
	for filename in filelist:
		shutil.move(filename, folders['rawdata'])

	filelist = glob.glob('model_*.out.txt')
	for filename in filelist:
		shutil.move(filename, folders['rawdata'])

	# archive figures
	filelist = glob.glob('figure_*.eps')
	for filename in filelist:
		shutil.move(filename, folders['figures'])

	# archive reports
	filelist = glob.glob('report_*.txt')
	for filename in filelist:
		shutil.move(filename, folders['reports'])

	# archive a log file
	log_file = 'log_{:s}.txt'.format(opts['systime'])
	with open(log_file, 'w') as file:
		file.write('# Output of {:s} {:s}\n'.format(opts['python'], subprocess.list2cmdline(sys.argv[0:])))
	shutil.move(log_file, results)
	shutil.copy2(opts['model'], results)

	return 0

if __name__ == '__main__':
	sbatch_error = b'sbatch: error: slurm_receive_msg: Socket timed out on send/recv operation\n' \
		b'sbatch: error: Batch job submission failed: Socket timed out on send/recv operation'
	squeue_error = b'squeue: error: slurm_receive_msg: Socket timed out on send/recv operation\n' \
		b'slurm_load_jobs error: Socket timed out on send/recv operation'
	#sbatch_error = b'sbatch: error: Slurm temporarily unable to accept job, sleeping and retrying.'
	#sbatch_error = b'sbatch: error: Batch job submission failed: Resource temporarily unavailable'

	# general options
	args = argsparser()
	opts = ga_opts()

	# perform safe checks prior to any calculation
	safe_checks()

	# clean the working directory
	clean()

	# read model configuration
	parameters = configurate()

	# Sterope Main Algorithm
	# generate an omega grid of N(2k + k) samples
	population = populate()
	# simulate levels
	population = simulate()
	# evaluate sensitivity
	sensitivity = evaluate()
	# plot and rank
	sensitivity = ranking()

	# move and organize results
	backup()
