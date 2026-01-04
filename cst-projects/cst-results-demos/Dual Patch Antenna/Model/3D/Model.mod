'# MWS Version: Version 2024.5 - Jun 14 2024 - ACIS 33.0.1 -

'# length = mm
'# frequency = GHz
'# time = ns
'# frequency range: fmin = 4 fmax = 7


'@ set workplane properties

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With WCS
     .SetWorkplaneSize "50" 
     .SetWorkplaneRaster "5" 
     .SetWorkplaneSnap "TRUE" 
     .SetWorkplaneSnapRaster "1" 
     .SetWorkplaneAutoadjust "TRUE" 
End With

'@ new component: component1

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Component.New "component1"

'@ define brick: component1:solid1

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Brick
     .Reset 
     .Name "solid1" 
     .Component "component1" 
     .Material "PEC" 
     .Xrange "0", "12" 
     .Yrange "0", "16" 
     .Zrange "0", "0.05" 
     .Create
End With

'@ store picked point: 1

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.NextPickToDatabase "1" 
Pick.PickEndpointFromId "component1:solid1", "1"

'@ define brick: component1:solid2

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Brick
     .Reset 
     .Name "solid2" 
     .Component "component1" 
     .Material "PEC" 
     .Xrange "2", "4" 
     .Yrange "-10", "0" 
     .Zrange "0", "zp(1)" 
     .Create
End With

'@ transform: mirror component1:solid1

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Transform 
     .Reset 
     .Name "component1:solid1" 
     .Origin "Free" 
     .Center "-5", "0", "0" 
     .PlaneNormal "1", "0", "0" 
     .MultipleObjects "True" 
     .GroupObjects "False" 
     .Repetitions "1" 
     .MultipleSelection "True" 
     .Component "" 
     .Material "" 
     .MirrorAdvanced 
End With

'@ transform: mirror component1:solid2

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Transform 
     .Reset 
     .Name "component1:solid2" 
     .Origin "Free" 
     .Center "-5", "0", "0" 
     .PlaneNormal "1", "0", "0" 
     .MultipleObjects "True" 
     .GroupObjects "False" 
     .Repetitions "1" 
     .MultipleSelection "False" 
     .Component "" 
     .Material "" 
     .MirrorAdvanced 
End With

'@ store picked point: 2

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.NextPickToDatabase "2" 
Pick.PickMidpointFromId "component1:solid1_1", "1"

'@ snap point to drawplane

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.SnapLastPointToDrawplane

'@ store picked point: 3

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.NextPickToDatabase "3" 
Pick.PickMidpointFromId "component1:solid1", "1"

'@ snap point to drawplane

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.SnapLastPointToDrawplane

'@ store picked point: 4

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.NextPickToDatabase "4" 
Pick.PickEndpointFromId "component1:solid2", "6"

'@ snap point to drawplane

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.SnapLastPointToDrawplane

'@ define material: substrate

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Material 
     .Reset 
     .Name "substrate"
     .FrqType "all" 
     .Type "Normal" 
     .Epsilon "4.2" 
     .Mue "1" 
     .Kappa "0" 
     .TanD "0.0" 
     .TanDFreq "0.0" 
     .TanDGiven "False" 
     .TanDModel "ConstTanD" 
     .KappaM "0" 
     .TanDM "0.0" 
     .TanDMFreq "0.0" 
     .TanDMGiven "False" 
     .TanDMModel "ConstTanD" 
     .DispModelEps "None" 
     .DispModelMue "None" 
     .DispersiveFittingSchemeEps "General 1st" 
     .DispersiveFittingSchemeMue "General 1st" 
     .UseGeneralDispersionEps "False" 
     .UseGeneralDispersionMue "False" 
     .Rho "0" 
     .ThermalType "Normal" 
     .ThermalConductivity "0" 
     .Colour "0", "1", "1" 
     .Wireframe "False" 
     .Transparency "0" 
     .Create
End With

'@ define brick: component1:solid3

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Brick
     .Reset 
     .Name "solid3" 
     .Component "component1" 
     .Material "substrate" 
     .Xrange "xp(2)-xy", "xp(3)+xy" 
     .Yrange "yp(2) - 0.5*(2.0*ldist2d(4, xp(2), yp(2), xp(3), yp(3)))", "yp(2) + 0.5*(2.0*ldist2d(4, xp(2), yp(2), xp(3), yp(3)))" 
     .Zrange "-1", "0" 
     .Create
End With

'@ pick face

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.PickFaceFromId "component1:solid2_1", "3"

'@ define port: 1

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Port 
     .Reset 
     .PortNumber "1" 
     .NumberOfModes "1" 
     .AdjustPolarization False 
     .PolarizationAngle "0.0" 
     .ReferencePlaneDistance "0" 
     .TextSize "50" 
     .Coordinates "Picks" 
     .Orientation "positive" 
     .PortOnBound "True" 
     .ClipPickedPortToBound "False" 
     .Xrange "-14", "-12" 
     .Yrange "-10", "-10" 
     .Zrange "0", "0.05" 
     .XrangeAdd "6", "6" 
     .YrangeAdd "0.0", "0.0" 
     .ZrangeAdd "1", "6" 
     .SingleEnded "False" 
     .Create 
End With

'@ pick face

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.PickFaceFromId "component1:solid2", "3"

'@ define port: 2

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Port 
     .Reset 
     .PortNumber "2" 
     .NumberOfModes "1" 
     .AdjustPolarization False 
     .PolarizationAngle "0.0" 
     .ReferencePlaneDistance "0" 
     .TextSize "50" 
     .Coordinates "Picks" 
     .Orientation "positive" 
     .PortOnBound "True" 
     .ClipPickedPortToBound "False" 
     .Xrange "2", "4" 
     .Yrange "-10", "-10" 
     .Zrange "0", "0.05" 
     .XrangeAdd "6", "6" 
     .YrangeAdd "0.0", "0.0" 
     .ZrangeAdd "1", "6" 
     .SingleEnded "False" 
     .Create 
End With

'@ use template: Antenna (on Planar Substrate)

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
' Template for Antenna on Planar Substrate
' ========================================
' (CSTxMWSxONLY)
' draw the bounding box
Plot.DrawBox True
' set units to mm, ghz
With Units 
     .Geometry "mm" 
     .Frequency "ghz" 
     .Time "ns" 
End With 
' set background material to vacuum
With Background 
     .Type "Normal" 
     .Epsilon "1.0" 
     .Mue "1.0" 
     .XminSpace "0.0" 
     .XmaxSpace "0.0" 
     .YminSpace "0.0" 
     .YmaxSpace "0.0" 
     .ZminSpace "0.0" 
     .ZmaxSpace "0.0" 
End With 
' set boundary conditions to open, zmin to electric
With Boundary
     .Xmin "open" 
     .Xmax "open" 
     .Ymin "open" 
     .Ymax "open" 
     .Zmin "electric" 
     .Zmax "expanded open" 
     .Xsymmetry "none" 
     .Ysymmetry "none" 
     .Zsymmetry "none" 
End With
' optimize mesh settings for planar structures
With Mesh 
     .MergeThinPECLayerFixpoints "True" 
     .RatioLimit "50" 
     .AutomeshRefineAtPecLines "True", "4"
     .FPBAAvoidNonRegUnite "True" 
End With 
' change mesh adaption scheme to energy 
' 		(planar structures tend to store high energy 
'     	 locally at edges rather than globally in volume)
MeshAdaption3D.SetAdaptionStrategy "Energy" 
' switch on FD-TET setting for accurate farfields
FDSolver.ExtrudeOpenBC "True"

'@ pick face

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Pick.PickFaceFromId "component1:solid3", "2"

'@ define extrude: component1:solid4

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Extrude 
     .Reset 
     .Name "solid4" 
     .Component "component1" 
     .Material "PEC" 
     .Mode "Picks" 
     .Height "0.05" 
     .Twist "0.0" 
     .Taper "0.0" 
     .UsePicksForHeight "False" 
     .DeleteBaseFaceSolid "False" 
     .ClearPickedFace "True" 
     .Create 
End With

'@ define boundaries

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Boundary
     .Xmin "expanded open" 
     .Xmax "expanded open" 
     .Ymin "expanded open" 
     .Ymax "expanded open" 
     .Zmin "expanded open" 
     .Zmax "expanded open" 
     .Xsymmetry "none" 
     .Ysymmetry "none" 
     .Zsymmetry "none" 
     .XminThermal "isothermal" 
     .XmaxThermal "isothermal" 
     .YminThermal "isothermal" 
     .YmaxThermal "isothermal" 
     .ZminThermal "isothermal" 
     .ZmaxThermal "isothermal" 
     .XsymmetryThermal "none" 
     .YsymmetryThermal "none" 
     .ZsymmetryThermal "none" 
     .ApplyInAllDirections "True" 
     .XminTemperature "" 
     .XminTemperatureType "None" 
     .XmaxTemperature "" 
     .XmaxTemperatureType "None" 
     .YminTemperature "" 
     .YminTemperatureType "None" 
     .YmaxTemperature "" 
     .YmaxTemperatureType "None" 
     .ZminTemperature "" 
     .ZminTemperatureType "None" 
     .ZmaxTemperature "" 
     .ZmaxTemperatureType "None" 
End With

'@ switch working plane

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Plot.DrawWorkplane "false"

'@ define frequency range

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Solver.FrequencyRange "4", "7"

'@ define monitor: e-field (f=5.632)

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Monitor 
     .Reset 
     .Name "e-field (f=5.632)" 
     .Dimension "Volume" 
     .Domain "Frequency" 
     .FieldType "Efield" 
     .Frequency "5.632" 
     .Create 
End With

'@ define monitor: h-field (f=5.632)

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Monitor 
     .Reset 
     .Name "h-field (f=5.632)" 
     .Dimension "Volume" 
     .Domain "Frequency" 
     .FieldType "Hfield" 
     .Frequency "5.632" 
     .Create 
End With

'@ define farfield monitor: farfield (f=5.632)

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With Monitor 
     .Reset 
     .Name "farfield (f=5.632)" 
     .Domain "Frequency" 
     .FieldType "Farfield" 
     .Frequency "5.632" 
     .Create 
End With

'@ set mesh properties (Hexahedral)

'[VERSION]2014.0|23.0.0|20130901[/VERSION]
With Mesh 
     .MeshType "PBA" 
     .SetCreator "High Frequency"
End With 
With MeshSettings 
     .SetMeshType "Hex" 
     .Set "Version", 1%
     'MAX CELL - WAVELENGTH REFINEMENT 
     .Set "StepsPerWaveNear", "10" 
     .Set "StepsPerWaveFar", "10" 
     .Set "WavelengthRefinementSameAsNear", "1" 
     'MAX CELL - GEOMETRY REFINEMENT 
     .Set "StepsPerBoxNear", "10" 
     .Set "StepsPerBoxFar", "1" 
     .Set "MaxStepNear", "0" 
     .Set "MaxStepFar", "0" 
     .Set "ModelBoxDescrNear", "maxedge" 
     .Set "ModelBoxDescrFar", "maxedge" 
     .Set "UseMaxStepAbsolute", "0" 
     .Set "GeometryRefinementSameAsNear", "0" 
     'MIN CELL 
     .Set "UseRatioLimitGeometry", "1" 
     .Set "RatioLimitGeometry", "10" 
     .Set "MinStepGeometryX", "0" 
     .Set "MinStepGeometryY", "0" 
     .Set "MinStepGeometryZ", "0" 
     .Set "UseSameMinStepGeometryXYZ", "1" 
End With 
With MeshSettings 
     .SetMeshType "Hex" 
     .Set "FaceRefinementOn", "0" 
     .Set "FaceRefinementPolicy", "2" 
     .Set "FaceRefinementRatio", "2" 
     .Set "FaceRefinementStep", "0" 
     .Set "FaceRefinementNSteps", "2" 
     .Set "EllipseRefinementOn", "0" 
     .Set "EllipseRefinementPolicy", "2" 
     .Set "EllipseRefinementRatio", "2" 
     .Set "EllipseRefinementStep", "0" 
     .Set "EllipseRefinementNSteps", "2" 
     .Set "FaceRefinementBufferLines", "3" 
     .Set "EdgeRefinementOn", "1" 
     .Set "EdgeRefinementPolicy", "1" 
     .Set "EdgeRefinementRatio", "4" 
     .Set "EdgeRefinementStep", "0" 
     .Set "EdgeRefinementBufferLines", "3" 
     .Set "RefineEdgeMaterialGlobal", "0" 
     .Set "RefineAxialEdgeGlobal", "0" 
     .Set "BufferLinesNear", "3" 
     .Set "UseDielectrics", "1" 
     .Set "EquilibrateOn", "0" 
     .Set "Equilibrate", "1.5" 
     .Set "IgnoreThinPanelMaterial", "0" 
     .Set "RefineEdgesAtBoundary", "0" 
End With 
With MeshSettings 
     .SetMeshType "Hex" 
     .Set "SnapToAxialEdges", "1"
     .Set "SnapToPlanes", "1"
     .Set "SnapToSpheres", "1"
     .Set "SnapToEllipses", "1"
     .Set "SnapToCylinders", "1"
     .Set "SnapToCylinderCenters", "1"
     .Set "SnapToEllipseCenters", "1"
End With 
With Discretizer 
     .MeshType "PBA" 
     .PBAType "Fast PBA" 
     .AutomaticPBAType "True" 
     .FPBAAccuracyEnhancement "enable"
     .ConnectivityCheck "False"
     .ConvertGeometryDataAfterMeshing "True" 
     .UsePecEdgeModel "True" 
     .GapDetection "False" 
     .FPBAGapTolerance "1e-3" 
     .SetMaxParallelMesherThreads "Hex", "8"
     .SetParallelMesherMode "Hex", "Maximum"
     .PointAccEnhancement "0" 
     .UseSplitComponents "True" 
     .EnableSubgridding "False" 
     .PBAFillLimit "99" 
     .AlwaysExcludePec "False" 
End With

'@ set units in materials

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
Material.SetUnitInMaterial "substrate", "GHz", "mm"

'@ farfield plot options

'[VERSION]2010.0|20.0.0|20090230[/VERSION]
With FarfieldPlot 
     .Plottype "3D" 
     .Vary "angle1" 
     .Theta "0" 
     .Phi "0" 
     .Step "5" 
     .Step2 "5" 
     .SetLockSteps "True" 
     .SetPlotRangeOnly "False" 
     .SetThetaStart "0" 
     .SetThetaEnd "180" 
     .SetPhiStart "0" 
     .SetPhiEnd "360" 
     .SetTheta360 "True" 
     .SymmetricRange "True" 
     .SetTimeDomainFF "False" 
     .SetFrequency "5.632" 
     .SetTime "0" 
     .SetColorByValue "True" 
     .DrawStepLines "False" 
     .DrawIsoLongitudeLatitudeLines "False" 
     .ShowStructure "False" 
     .SetStructureTransparent "False" 
     .SetFarfieldTransparent "False" 
     .SetPlotMode "Gain" 
     .Distance "1" 
     .UseFarfieldApproximation "True" 
     .SetScaleLinear "False" 
     .SetLogRange "40" 
     .SetLogNorm "0" 
     .DBUnit "0" 
     .EnableFixPlotMaximum "False" 
     .SetFixPlotMaximumValue "1.0" 
     .SetInverseAxialRatio "False" 
     .SetAxesType "user" 
     .Phistart "1.000000e+000", "0.000000e+000", "0.000000e+000" 
     .Thetastart "0.000000e+000", "0.000000e+000", "1.000000e+000" 
     .PolarizationVector "0.000000e+000", "1.000000e+000", "0.000000e+000" 
     .SetCoordinateSystemType "spherical" 
     .SetPolarizationType "Linear" 
     .SlantAngle 0.000000e+000 
     .Origin "bbox" 
     .Userorigin "0.000000e+000", "0.000000e+000", "0.000000e+000" 
     .SetUserDecouplingPlane "False" 
     .UseDecouplingPlane "False" 
     .DecouplingPlaneAxis "X" 
     .DecouplingPlanePosition "0.000000e+000" 
     .EnablePhaseCenterCalculation "False" 
     .SetPhaseCenterAngularLimit "3.000000e+001" 
     .SetPhaseCenterComponent "boresight" 
     .SetPhaseCenterPlane "both" 
     .ShowPhaseCenter "True" 
     .StoreSettings
End With

'@ define solver parameters

'[VERSION]2011.0|21.0.0|20100920[/VERSION]
Mesh.SetCreator "High Frequency" 
With Solver 
     .CalculationType "TD-S"
     .StimulationPort "All"
     .StimulationMode "All"
     .SteadyStateLimit "-40"
     .MeshAdaption "False"
     .AutoNormImpedance "False"
     .NormingImpedance "50"
     .CalculateModesOnly "False"
     .SParaSymmetry "False"
     .StoreTDResultsInCache  "False"
     .FullDeembedding "False"
     .SuperimposePLWExcitation "False"
     .UseSensitivityAnalysis "False"
End With

'@ set mesh properties

'[VERSION]2013.0|23.0.0|20130115[/VERSION]
With MeshSettings 
     .SetMeshType "Tet" 
     .Set "CellsPerWavelengthPolicy", "cellsperwavelength" 
     .Set "CurvatureOrderPolicy", "off" 
     .SetMeshType "Plane" 
     .Set "CurvatureOrderPolicy", "off" 
End With

'@ change solver type

'[VERSION]2013.0|23.0.0|20130115[/VERSION]
ChangeSolverType "HF Time Domain"

'@ set pba mesh type

'[VERSION]2014.0|23.0.0|20130901[/VERSION]
Mesh.MeshType "PBA"

'@ define time domain solver parameters

'[VERSION]2014.0|23.0.0|20130901[/VERSION]
Mesh.SetCreator "High Frequency" 
With Solver 
     .Method "Hexahedral"
     .CalculationType "TD-S"
     .StimulationPort "All"
     .StimulationMode "All"
     .SteadyStateLimit "-40"
     .MeshAdaption "False"
     .AutoNormImpedance "False"
     .NormingImpedance "50"
     .CalculateModesOnly "False"
     .SParaSymmetry "False"
     .StoreTDResultsInCache  "False"
     .FullDeembedding "False"
     .SuperimposePLWExcitation "False"
     .UseSensitivityAnalysis "False"
End With

'@ set pba mesh type

'[VERSION]2014.0|23.0.0|20130901[/VERSION]
Mesh.MeshType "PBA"

'@ set mesh properties (for backward compatibility)

'[VERSION]2016.0|25.0.2|20150831[/VERSION]
With MeshSettings 
    .SetMeshType "Hex"
    .Set "PlaneMergeVersion", 0
End With

'@ define special time domain solver parameters

'[VERSION]2018.0|27.0.2|20170822[/VERSION]
'STEADY STATE
With Solver
     .SteadyStateDurationType "Number of pulses"
     .NumberOfPulseWidths "20"
     .SteadyStateDurationTime "5.41692"
     .SteadyStateDurationTimeAsDistance "1625.08"
     .StopCriteriaShowExcitation "False"
     .RemoveAllStopCriteria
     .AddStopCriterion "All S-Parameters", "0.004", "1", "False"
     .AddStopCriterion "Transmission S-Parameters", "0.004", "1", "False"
     .AddStopCriterion "Reflection S-Parameters", "0.004", "1", "False"
     .AddStopCriterion "All Probes", "0.004", "1", "False"
     .AddStopCriterion "All Radiated Powers", "0.004", "1", "False"
End With
'GENERAL
With Solver
     .TimeStepStabilityFactor "1.0"
     .RestartAfterInstabilityAbort "True"
     .AutomaticTimeSignalSampling "True"
     .SuppressTimeSignalStorage "False"
     .ConsiderExcitationForFreqSamplingRate "False"
     .UseBroadBandPhaseShift "False"
     .SetBroadBandPhaseShiftLowerBoundFac "0.1"
     .SetPortShieldingType "NONE"
     .FrequencySamples "1001"
     .FrequencyLogSamples "0"
     .ConsiderTwoPortReciprocity "True"
     .EnergyBalanceLimit "0.03"
     .TDRComputation "False"
     .TDRShift50Percent "False"
     .AutoDetectIdenticalPorts "False"
End With
'HEXAHEDRAL
With Solver
     .SetPMLType "CONVPML"
     .UseVariablePMLLayerSizeStandard "False"
     .KeepPMLDepthDuringMeshAdaptationWithVariablePMLLayerSize "False"
     .SetSubcycleState "Automatic"
     .NormalizeToReferenceSignal "True"
     .SetEnhancedPMLStabilization "Automatic"
     .SimplifiedPBAMethod "False"
     .SParaAdjustment "True"
     .PrepareFarfields "True"
     .MonitorFarFieldsNearToModel "False"
     .DiscreteItemUpdate "Distributed"
End With
'MATERIAL
With Solver
     .SurfaceImpedanceOrder "10"
     .ActivatePowerLoss1DMonitor "True"
     .PowerLoss1DMonitorPerSolid "False"
     .Use3DFieldMonitorForPowerLoss1DMonitor "True"
     .UseFarFieldMonitorForPowerLoss1DMonitor "False"
     .UseExtraFreqForPowerLoss1DMonitor "False"
     .ResetPowerLoss1DMonitorExtraFreq
     .SetDispNonLinearMaterialMonitor "False"
     .ActivateDispNonLinearMaterialMonitor "0.0",  "0.02",  "0.0",  "False"
     .SetTimePowerLossSIMaterialMonitor "False"
     .ActivateTimePowerLossSIMaterialMonitor "0.0",  "0.02",  "0.0",  "False"
     .SetTimePowerLossSIMaterialMonitorAverage "False"
     .SetTimePowerLossSIMaterialMonitorAverageRepPeriod "0.0"
     .TimePowerLossSIMaterialMonitorPerSolid "False"
     .ActivateSpaceMaterial3DMonitor "False"
     .Use3DFieldMonitorForSpaceMaterial3DMonitor "True"
     .UseExtraFreqForSpaceMaterial3DMonitor "False"
     .ResetSpaceMaterial3DMonitorExtraFreq
     .SetHFTDDispUpdateScheme "Standard"
End With
'AR-FILTER
With Solver
     .UseArfilter "False"
     .ArMaxEnergyDeviation "0.1"
     .ArPulseSkip "1"
End With
'WAVEGUIDE
With Solver
     .WaveguidePortGeneralized "True"
     .WaveguidePortModeTracking "False"
     .WaveguidePortROM "False"
     .DispEpsFullDeembedding "False"
     .SetSamplesFullDeembedding "20"
     .AbsorbUnconsideredModeFields "Automatic"
     .SetModeFreqFactor "0.5"
     .AdaptivePortMeshing "True"
     .AccuracyAdaptivePortMeshing "1"
     .PassesAdaptivePortMeshing "4"
End With
'HEXAHEDRAL TLM
With Solver
     .AnisotropicSheetSurfaceType "0"
     .UseMeshType "1"
     .UseAbsorbingBoundary "True"
     .UseDoublePrecision "False"
     .AllowMaterialOverlap "True"
     .ExcitePlanewaveNearModel "False"
     .SetGroundPlane "False"
     .GroundPlane "x", "0.0"
     .NumberOfLayers "5"
     .HealCheckAllObjects "False"
     .NormalizeToGaussian "True"
     .TimeSignalSamplingFactor "1"
End With
'TLM POSTPROCESSING
With Solver
     .ResetSettings
     .CalculateNearFieldOnCylindricalSurfaces "false", "Coarse" 
     .CylinderGridCustomStep "1" 
     .CalculateNearFieldOnCircularCuts "false" 
     .CylinderBaseCenter "0", "0", "0" 
     .CylinderRadius "3" 
     .CylinderHeight "3" 
     .CylinderSpacing "1" 
     .CylinderResolution "2.0" 
     .CylinderAllPolarization "true" 
     .CylinderRadialAngularVerticalComponents "false" 
     .CylinderMagnitudeOfTangentialConponent "false" 
     .CylinderVm "true" 
     .CylinderDBVm "false" 
     .CylinderDBUVm "false" 
     .CylinderAndFrontAxes "+y", "+z" 
     .ApplyLinearPrediction "false" 
     .Windowing "None" 
     .LogScaleFrequency "false" 
     .AutoFreqStep "true", "1"
     .SetExcitationSignal "" 
     .SaveSettings
End With

'@ set PBA version

'[VERSION]2019.0|28.0.1|20180326[/VERSION]
Discretizer.PBAVersion "2017082218"

'@ define special time domain solver parameters

'[VERSION]2019.0|28.0.1|20180326[/VERSION]
'STEADY STATE
With Solver
     .SteadyStateDurationType "Number of pulses"
     .NumberOfPulseWidths "20"
     .SteadyStateDurationTime "5.41692"
     .SteadyStateDurationTimeAsDistance "1625.08"
     .StopCriteriaShowExcitation "False"
     .RemoveAllStopCriteria
     .AddStopCriterion "All S-Parameters", "0.004", "1", "False"
     .AddStopCriterion "Transmission S-Parameters", "0.004", "1", "False"
     .AddStopCriterion "Reflection S-Parameters", "0.004", "1", "False"
     .AddStopCriterion "All Probes", "0.004", "1", "False"
     .AddStopCriterion "All Radiated Powers", "0.004", "1", "False"
End With
'GENERAL
With Solver
     .TimeStepStabilityFactor "1.0"
     .RestartAfterInstabilityAbort "True"
     .AutomaticTimeSignalSampling "True"
     .SuppressTimeSignalStorage "False"
     .ConsiderExcitationForFreqSamplingRate "False"
     .UseBroadBandPhaseShift "False"
     .SetBroadBandPhaseShiftLowerBoundFac "0.1"
     .SetPortShieldingType "NONE"
     .FrequencySamples "1001"
     .FrequencyLogSamples "0"
     .ConsiderTwoPortReciprocity "True"
     .EnergyBalanceLimit "0.03"
     .TDRComputation "False"
     .TDRShift50Percent "False"
     .AutoDetectIdenticalPorts "False"
End With
'HEXAHEDRAL
With Solver
     .SetPMLType "CONVPML"
     .UseVariablePMLLayerSizeStandard "False"
     .KeepPMLDepthDuringMeshAdaptationWithVariablePMLLayerSize "False"
     .SetSubcycleState "Automatic"
     .NormalizeToReferenceSignal "True"
     .SetEnhancedPMLStabilization "Automatic"
     .SimplifiedPBAMethod "False"
     .SParaAdjustment "True"
     .PrepareFarfields "True"
     .MonitorFarFieldsNearToModel "True"
     .DiscreteItemUpdate "Distributed"
End With
'MATERIAL
With Solver
     .SurfaceImpedanceOrder "10"
     .ActivatePowerLoss1DMonitor "True"
     .PowerLoss1DMonitorPerSolid "False"
     .Use3DFieldMonitorForPowerLoss1DMonitor "True"
     .UseFarFieldMonitorForPowerLoss1DMonitor "False"
     .UseExtraFreqForPowerLoss1DMonitor "False"
     .ResetPowerLoss1DMonitorExtraFreq
     .SetDispNonLinearMaterialMonitor "False"
     .ActivateDispNonLinearMaterialMonitor "0.0",  "0.02",  "0.0",  "False"
     .SetTimePowerLossSIMaterialMonitor "False"
     .ActivateTimePowerLossSIMaterialMonitor "0.0",  "0.02",  "0.0",  "False"
     .SetTimePowerLossSIMaterialMonitorAverage "False"
     .SetTimePowerLossSIMaterialMonitorAverageRepPeriod "0.0"
     .TimePowerLossSIMaterialMonitorPerSolid "False"
     .ActivateSpaceMaterial3DMonitor "False"
     .Use3DFieldMonitorForSpaceMaterial3DMonitor "True"
     .UseExtraFreqForSpaceMaterial3DMonitor "False"
     .ResetSpaceMaterial3DMonitorExtraFreq
     .SetHFTDDispUpdateScheme "Standard"
End With
'AR-FILTER
With Solver
     .UseArfilter "False"
     .ArMaxEnergyDeviation "0.1"
     .ArPulseSkip "1"
End With
'WAVEGUIDE
With Solver
     .WaveguidePortGeneralized "True"
     .WaveguidePortModeTracking "False"
     .WaveguidePortROM "False"
     .DispEpsFullDeembedding "False"
     .SetSamplesFullDeembedding "20"
     .AbsorbUnconsideredModeFields "Automatic"
     .SetModeFreqFactor "0.5"
     .AdaptivePortMeshing "True"
     .AccuracyAdaptivePortMeshing "1"
     .PassesAdaptivePortMeshing "4"
End With
'HEXAHEDRAL TLM
With Solver
     .AnisotropicSheetSurfaceType "0"
     .UseMeshType "1"
     .UseAbsorbingBoundary "True"
     .UseDoublePrecision "False"
     .AllowMaterialOverlap "True"
     .ExcitePlanewaveNearModel "False"
     .SetGroundPlane "False"
     .GroundPlane "x", "0.0"
     .NumberOfLayers "5"
     .HealCheckAllObjects "False"
     .NormalizeToGaussian "True"
     .TimeSignalSamplingFactor "1"
End With
'TLM POSTPROCESSING
With Solver
     .ResetSettings
     .CalculateNearFieldOnCylindricalSurfaces "false", "Coarse" 
     .CylinderGridCustomStep "1" 
     .CalculateNearFieldOnCircularCuts "false" 
     .CylinderBaseCenter "0", "0", "0" 
     .CylinderRadius "3" 
     .CylinderHeight "3" 
     .CylinderSpacing "1" 
     .CylinderResolution "2.0" 
     .CylinderAllPolarization "true" 
     .CylinderRadialAngularVerticalComponents "false" 
     .CylinderMagnitudeOfTangentialConponent "false" 
     .CylinderVm "true" 
     .CylinderDBVm "false" 
     .CylinderDBUVm "false" 
     .CylinderAndFrontAxes "+y", "+z" 
     .ApplyLinearPrediction "false" 
     .Windowing "None" 
     .LogScaleFrequency "false" 
     .AutoFreqStep "true", "1"
     .SetExcitationSignal "" 
     .SaveSettings
End With
'TETRAHEDRAL
With Solver
     With .SolverSettings ("time domain")
          .SetMeshType "Tetrahedral" 
          .Set "Discretization", "Automatic" 
     End With 
End With

'@ set mesh properties (Hexahedral)

'[VERSION]2019.0|28.0.2|20180814[/VERSION]
With Mesh 
     .MeshType "PBA" 
     .SetCreator "High Frequency"
End With 
With MeshSettings 
     .SetMeshType "Hex" 
     .Set "Version", 1%
     'MAX CELL - WAVELENGTH REFINEMENT 
     .Set "StepsPerWaveNear", "10" 
     .Set "StepsPerWaveFar", "10" 
     .Set "WavelengthRefinementSameAsNear", "1" 
     'MAX CELL - GEOMETRY REFINEMENT 
     .Set "StepsPerBoxNear", "10" 
     .Set "StepsPerBoxFar", "1" 
     .Set "MaxStepNear", "0" 
     .Set "MaxStepFar", "0" 
     .Set "ModelBoxDescrNear", "maxedge" 
     .Set "ModelBoxDescrFar", "maxedge" 
     .Set "UseMaxStepAbsolute", "0" 
     .Set "GeometryRefinementSameAsNear", "0" 
     'MIN CELL 
     .Set "UseRatioLimitGeometry", "1" 
     .Set "RatioLimitGeometry", "10" 
     .Set "MinStepGeometryX", "0" 
     .Set "MinStepGeometryY", "0" 
     .Set "MinStepGeometryZ", "0" 
     .Set "UseSameMinStepGeometryXYZ", "1" 
End With 
With MeshSettings 
     .Set "PlaneMergeVersion", "2" 
End With 
With MeshSettings 
     .SetMeshType "Hex" 
     .Set "FaceRefinementOn", "0" 
     .Set "FaceRefinementPolicy", "2" 
     .Set "FaceRefinementRatio", "2" 
     .Set "FaceRefinementStep", "0" 
     .Set "FaceRefinementNSteps", "2" 
     .Set "EllipseRefinementOn", "0" 
     .Set "EllipseRefinementPolicy", "2" 
     .Set "EllipseRefinementRatio", "2" 
     .Set "EllipseRefinementStep", "0" 
     .Set "EllipseRefinementNSteps", "2" 
     .Set "FaceRefinementBufferLines", "3" 
     .Set "EdgeRefinementOn", "1" 
     .Set "EdgeRefinementPolicy", "1" 
     .Set "EdgeRefinementRatio", "4" 
     .Set "EdgeRefinementStep", "0" 
     .Set "EdgeRefinementBufferLines", "3" 
     .Set "RefineEdgeMaterialGlobal", "0" 
     .Set "RefineAxialEdgeGlobal", "0" 
     .Set "BufferLinesNear", "3" 
     .Set "UseDielectrics", "1" 
     .Set "EquilibrateOn", "0" 
     .Set "Equilibrate", "1.5" 
     .Set "IgnoreThinPanelMaterial", "0" 
End With 
With MeshSettings 
     .SetMeshType "Hex" 
     .Set "SnapToAxialEdges", "1"
     .Set "SnapToPlanes", "1"
     .Set "SnapToSpheres", "1"
     .Set "SnapToEllipses", "1"
     .Set "SnapToCylinders", "1"
     .Set "SnapToCylinderCenters", "1"
     .Set "SnapToEllipseCenters", "1"
End With 
With Discretizer 
     .ConnectivityCheck "True"
     .UsePecEdgeModel "True" 
     .GapDetection "True" 
     .FPBAGapTolerance "1e-3" 
     .PointAccEnhancement "0" 
     .TSTVersion "2"
	  .PBAVersion "2017082218" 
End With

'@ set solver type

'[VERSION]2019.0|28.0.2|20180823[/VERSION]
SetSolverType "HF_TRANSIENT" 

