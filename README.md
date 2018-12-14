This README document is meant solely for the purpose of giving explicit instruction on how to run examples.

For anything else, please see the included Colored Petri Net report.

First, please open a new project from the ColoredPetriNetDeveloper seed. Then click into the "Network" component. Intructions are available within this "Instructions" component if needed.

These instructions refer to the CPN Network example that is included with our model. However, they should generalize to all models.

NextStep: This plugin changes the model! As a result of running this plugin, the Tokens attribute of Places can be changed. The plugin gets the current state of the model and fires a Transition from the list of enabled Transitions. The result is then saved.

AllPossible: This plugin leaves the model largely unchanged. It does modify the StateSpace attribute of the CPN. If the Naked module is available, this plugin will create an HTML file for a visual trace of all states. If not, it will create and ejs file which can be compiled to the afore mentioned HTML file. The plugin gets the current state of the model and fires all possible Transitions, collects the resulting states, and then repeats the process until no new states are generated, no transitions can be fired from any state, or the maximum number of iterations are reached.

TotalRun: This plugin changes the model! As a result of running this plugin, the Tokens attribute of Places can be changed. If the Naked module is available, this plugin will create an HTML file for a visual trace of all states. If not, it will create and ejs file which can be compiled to the afore mentioned HTML file. The plugin gets the current state of the model and fires a Transition from the list of enabled Transitions. The process is then repeated for the resulting state. This process continues until no transitions are enabled or a maximum number of iterations are reached. The model is then saved to the final state.

IsDeterministic: This plugin leaves the model largely unchanged. It does modify the IsDeterministic attribute of the CPN. The plugin uses the same process as AllPossible, but terminates early if at any point more than one transition is enabled (yielding a result of False for IsDeterministic). Otherwise, it terminates if every new state generated has already been seen (yielding a result of True for IsDeterministic), or if no transitions are enabled (yielding a result of True for IsDeterministic). If the maximum number of iterations are reached, then the plugin terminates (yielding a result of True so far for IsDeterministic).

SetInitialState: This plugin leaves the model largetly unchanged. It does modify the InitialState attribute of the CPN, which is hidden. That attribute is utilized by the Reset plugin to reset the state of the model.

Reset: This plugin changes the model! As a result of running this plugin, the Tokens attribute of Places can be changed. This plugin sets the model to the state described by InitialState, a hidden attribute that is set by SetInitialState.

Furthermore, note that any plugin which changes the model is also going to change the IsDeterministic and StateSpace attributes, as these attributes are meant to describe the model for a given state.
