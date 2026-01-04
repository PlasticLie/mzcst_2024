'# MWS Version: Version 2024.5 - Jun 14 2024 - ACIS 33.0.1 -

'# length = mm
'# frequency = GHz
'# time = ns
'# frequency range: fmin = 4 fmax = 5
'# created = '[VERSION]2018.0|27.0.2|20170912[/VERSION]


'@ define units

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Units 
     .Geometry "mm" 
     .Frequency "GHz" 
     .Time "ns" 
     .TemperatureUnit "Kelvin" 
     .Voltage "V" 
     .Current "A" 
     .Resistance "Ohm" 
     .Conductance "Siemens" 
     .Capacitance "PikoF" 
     .Inductance "NanoH" 
End With

'@ set reference block coordinate system in assembly: Horn Antenna_1

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
SetWCSFromReferenceBlockInAssembly "Horn Antenna_1"

'@ transform local coordinates

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
TransformCurrentWCS "Horn Antenna_1", False

'@ import external project: ..\..\Model\DS\Block\0\B541087506\Horn Antenna.cst

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
StartSubProject 

With Material 
     .Reset 
     .Name "PEC" 
     .Folder "Horn Antenna_1" 
     .Rho "0"
     .ThermalType "PTC"
     .MechanicsType "Unused"
     .IntrinsicCarrierDensity "0"
     .FrqType "all"
     .Type "Pec"
     .MaterialUnit "Frequency", "Hz"
     .MaterialUnit "Geometry", "m"
     .MaterialUnit "Time", "s"
     .MaterialUnit "Temperature", "K"
     .Epsilon "1"
     .Mu "1"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Colour "0.8", "0.8", "0.8" 
     .Wireframe "False" 
     .Reflection "True" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .Create
End With 

With SAT
     .Reset 
     .FileName "*Horn Antenna^3D.sab" 
     .SubProjectName3D "..\..\Model\DS\Block\0\B541087506\Horn Antenna.cst" 
     .SubProjectScaleFactor "0.001" 
     .Version "11.0" 
     .PortnameMap "1>1" 
     .AssemblyPartName "Horn Antenna_1" 
     .ImportToActiveCoordinateSystem "True" 
     .Curves "True" 
     .Wires "True" 
     .SolidWiresAsSolids "False" 
     .ImportSources "True" 
     .Set "ImportSensitivityInformation", "False" 
     .Read 
End With

With Port 
     .Reset 
     .PortNumber "1" 
     .Label ""
     .Folder ""
     .NumberOfModes "1"
     .AdjustPolarization "False"
     .PolarizationAngle "0"
     .ReferencePlaneDistance "0"
     .TextSize "50"
     .TextMaxLimit "1"
     .Coordinates "Free"
     .Orientation "zmin"
     .PortOnBound "False"
     .ClipPickedPortToBound "False"
     .Xrange "0", "40"
     .Yrange "0", "20"
     .Zrange "0", "0"
     .XrangeAdd "0.0", "0.0"
     .YrangeAdd "0.0", "0.0"
     .ZrangeAdd "0.0", "0.0"
     .SingleEnded "False"
     .WaveguideMonitor "False"
     .ReferenceWCS "20", "10", "0", "0", "0", "-1", "0", "1", "0"
     .CreateImported 
End With 

With Transform 
     .Reset 
     .Name "port1" 
     .UseGlobalCoordinates "True" 
     .Vector "-20", "-10", "0" 
     .AdjustVectorToSubProjectScaleFactor 
     .Matrix "1", "0", "0", "0", "1", "0", "0", "0", "1" 
     .Transform "port", "matrix" 
     .Transform "port", "GlobalToLocal" 
End With 


EndSubProject 


'@ transform local coordinates

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
TransformCurrentWCS "Horn Antenna_1", True

'@ transform local coordinates

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
TransformCurrentWCS "Reflector Dish_1", False

'@ import external project: ..\..\Model\DS\Block\0\B117493488\Reflector Dish.cst

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
StartSubProject 

With Material 
     .Reset 
     .Name "PEC" 
     .Folder "Reflector Dish_1" 
     .Rho "0"
     .ThermalType "PTC"
     .MechanicsType "Unused"
     .IntrinsicCarrierDensity "0"
     .FrqType "all"
     .Type "Pec"
     .MaterialUnit "Frequency", "Hz"
     .MaterialUnit "Geometry", "m"
     .MaterialUnit "Time", "s"
     .MaterialUnit "Temperature", "K"
     .Epsilon "1"
     .Mu "1"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Colour "0.8", "0.8", "0.8" 
     .Wireframe "False" 
     .Reflection "True" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .Create
End With 

With SAT
     .Reset 
     .FileName "*Reflector Dish^3D.sab" 
     .SubProjectName3D "..\..\Model\DS\Block\0\B117493488\Reflector Dish.cst" 
     .SubProjectScaleFactor "1" 
     .Version "11.0" 
     .PortnameMap "" 
     .AssemblyPartName "Reflector Dish_1" 
     .ImportToActiveCoordinateSystem "True" 
     .Curves "True" 
     .Wires "True" 
     .SolidWiresAsSolids "False" 
     .ImportSources "True" 
     .Set "ImportSensitivityInformation", "False" 
     .Read 
End With


EndSubProject 


'@ transform local coordinates

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
TransformCurrentWCS "Reflector Dish_1", True

'@ define frequency range

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
Solver.FrequencyRange "4", "5"

'@ define background

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Background 
     .Reset 
     .XminSpace "0.0" 
     .XmaxSpace "0.0" 
     .YminSpace "0.0" 
     .YmaxSpace "0.0" 
     .ZminSpace "0.0" 
     .ZmaxSpace "1.5*100" 
     .ApplyInAllDirections "False" 
End With 
With Material 
     .Reset 
     .Rho "0.0"
     .ThermalType "Normal"
     .ThermalConductivity "0.0"
     .HeatCapacity "0.0"
     .DynamicViscosity "0.0"
     .Emissivity "0"
     .MetabolicRate "0.0"
     .VoxelConvection "0.0"
     .BloodFlow "0"
     .MechanicsType "Unused"
     .FrqType "all"
     .Type "Normal"
     .MaterialUnit "Frequency", "Hz"
     .MaterialUnit "Geometry", "m"
     .MaterialUnit "Time", "s"
     .MaterialUnit "Temperature", "Kelvin"
     .Epsilon "1.0"
     .Mu "1.0"
     .Sigma "0.0"
     .TanD "0.0"
     .TanDFreq "0.0"
     .TanDGiven "False"
     .TanDModel "ConstSigma"
     .EnableUserConstTanDModelOrderEps "False"
     .ConstTanDModelOrderEps "1"
     .SetElParametricConductivity "False"
     .ReferenceCoordSystem "Global"
     .CoordSystemType "Cartesian"
     .SigmaM "0"
     .TanDM "0.0"
     .TanDMFreq "0.0"
     .TanDMGiven "False"
     .TanDMModel "ConstSigma"
     .EnableUserConstTanDModelOrderMu "False"
     .ConstTanDModelOrderMu "1"
     .SetMagParametricConductivity "False"
     .DispModelEps  "None"
     .DispModelMu "None"
     .DispersiveFittingSchemeEps "Nth Order"
     .MaximalOrderNthModelFitEps "10"
     .ErrorLimitNthModelFitEps "0.1"
     .UseOnlyDataInSimFreqRangeNthModelEps "False"
     .DispersiveFittingSchemeMu "Nth Order"
     .MaximalOrderNthModelFitMu "10"
     .ErrorLimitNthModelFitMu "0.1"
     .UseOnlyDataInSimFreqRangeNthModelMu "False"
     .UseGeneralDispersionEps "False"
     .UseGeneralDispersionMu "False"
     .NonlinearMeasurementError "1e-1"
     .NLAnisotropy "False"
     .NLAStackingFactor "1"
     .NLADirectionX "1"
     .NLADirectionY "0"
     .NLADirectionZ "0"
     .Colour "0.6", "0.6", "0.6" 
     .Wireframe "False" 
     .Reflection "False" 
     .Allowoutline "True" 
     .Transparentoutline "False" 
     .Transparency "0" 
     .ChangeBackgroundMaterial
End With

'@ define boundaries

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Boundary 
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "magnetic"
     .Ysymmetry "electric"
     .Zsymmetry "none"
     .ApplyInAllDirections "False"
     .ThermalBoundary "Xmin", "isothermal"
     .ThermalBoundary "Xmax", "isothermal"
     .ThermalBoundary "Ymin", "isothermal"
     .ThermalBoundary "Ymax", "isothermal"
     .ThermalBoundary "Zmin", "isothermal"
     .ThermalBoundary "Zmax", "isothermal"
     .ThermalSymmetry "X", "symmetric"
     .ThermalSymmetry "Y", "symmetric"
     .ThermalSymmetry "Z", "none"
     .ResetThermalBoundaryValues
     .WallFlow "Xmin", "NoSlip"
     .WallFlow "Xmax", "NoSlip"
     .WallFlow "Ymin", "NoSlip"
     .WallFlow "Ymax", "NoSlip"
     .WallFlow "Zmin", "NoSlip"
     .WallFlow "Zmax", "NoSlip"
End With

'@ define frequency range

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
Solver.FrequencyRange "4", "5"

'@ define pml specials

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Boundary
.MinimumDistanceReferenceFrequencyType "CenterNMonitors"
End With

'@ define farfield monitor: farfield (f=5)

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
With Monitor 
     .Delete "farfield (f=fctr)" 
End With 
With Monitor 
     .Reset 
     .Name "farfield (f=5)" 
     .Domain "Frequency" 
     .FieldType "Farfield" 
     .Frequency "5" 
     .ExportFarfieldSource "False" 
     .UseSubvolume "False" 
     .Coordinates "Free" 
     .SetSubvolume "0.0", "0.0", "0.0", "0.0", "0.0", "0.0" 
     .SetSubvolumeOffset "0.0", "0.0", "0.0", "0.0", "0.0", "0.0" 
     .SetSubvolumeOffsetType "Absolute" 
     .Create 
End With

'@ define monitor: e-field (f=5)

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
With Monitor 
     .Delete "e-field (f=fctr)" 
End With 
With Monitor 
     .Reset 
     .Name "e-field (f=5)" 
     .Dimension "Volume" 
     .Domain "Frequency" 
     .FieldType "Efield" 
     .Frequency "5" 
     .UseSubvolume "False" 
     .Coordinates "Free" 
     .SetSubvolume "0.0", "0.0", "0.0", "0.0", "0.0", "0.0" 
     .SetSubvolumeOffset "0.0", "0.0", "0.0", "0.0", "0.0", "0.0" 
     .Create 
End With

'@ define monitor: h-field (f=5)

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
With Monitor 
     .Delete "h-field (f=fctr)" 
End With 
With Monitor 
     .Reset 
     .Name "h-field (f=5)" 
     .Dimension "Volume" 
     .Domain "Frequency" 
     .FieldType "Hfield" 
     .Frequency "5" 
     .UseSubvolume "False" 
     .Coordinates "Free" 
     .SetSubvolume "0.0", "0.0", "0.0", "0.0", "0.0", "0.0" 
     .SetSubvolumeOffset "0.0", "0.0", "0.0", "0.0", "0.0", "0.0" 
     .Create 
End With

'@ define solver parameters

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Solver 
.CalculationType "TD-S"
.StimulationPort "All"
.StimulationMode "All"
.SteadyStateLimit "-40"
.AdaptivePortMeshing False
End With

'@ (*) s-parameter post processing: vswr

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With PostProcess1D 
.ActivateOperation "vswr", "True"
End With

'@ (*) s-parameter post processing: yz-matrices

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With PostProcess1D 
.ActivateOperation "yz-matrices", "True"
End With

'@ set mesh properties (Hexahedral)

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With MeshSettings 
     .SetMeshType "Hex" 
     .Set "StepsPerWaveNear", "10" 
End With

'@ change solver type

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
ChangeSolverType "HF Time Domain"

'@ define units

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Units 
     .Geometry "mm" 
     .Frequency "GHz" 
     .Time "ns" 
     .TemperatureUnit "Kelvin" 
     .Voltage "V" 
     .Current "A" 
     .Resistance "Ohm" 
     .Conductance "Siemens" 
     .Capacitance "PikoF" 
     .Inductance "NanoH" 
End With

'@ activate global coordinates

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
WCS.ActivateWCS "global"

'@ change problem type

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
ChangeProblemType "High Frequency"

'@ set solver type

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
SetSolverType "HF_TRANSIENT" 
ChangeSolverType "HF Time Domain" 
With Solver
     .Method "Hexahedral"
End With

'@ define boundaries

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With Boundary
     .Xmin "expanded open"
     .Xmax "expanded open"
     .Ymin "expanded open"
     .Ymax "expanded open"
     .Zmin "expanded open"
     .Zmax "expanded open"
     .Xsymmetry "magnetic"
     .Ysymmetry "none"
     .Zsymmetry "none"
     .ApplyInAllDirections "False"
End With

'@ define time domain solver parameters

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
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

'@ farfield plot options

'[VERSION]2018.0|27.0.2|20170912[/VERSION]
With FarfieldPlot 
     .Plottype "3D" 
     .Vary "angle1" 
     .Theta "90" 
     .Phi "90" 
     .Step "1" 
     .Step2 "1" 
     .SetLockSteps "True" 
     .SetPlotRangeOnly "False" 
     .SetThetaStart "0" 
     .SetThetaEnd "180" 
     .SetPhiStart "0" 
     .SetPhiEnd "360" 
     .SetTheta360 "False" 
     .SymmetricRange "False" 
     .SetTimeDomainFF "False" 
     .SetFrequency "-1" 
     .SetTime "0" 
     .SetColorByValue "True" 
     .DrawStepLines "False" 
     .DrawIsoLongitudeLatitudeLines "False" 
     .ShowStructure "True" 
     .ShowStructureProfile "True" 
     .SetStructureTransparent "False" 
     .SetFarfieldTransparent "False" 
     .SetSpecials "enablepolarextralines" 
     .SetPlotMode "Directivity" 
     .Distance "1" 
     .UseFarfieldApproximation "True" 
     .SetScaleLinear "False" 
     .SetLogRange "40" 
     .SetLogNorm "0" 
     .DBUnit "0" 
     .EnableFixPlotMaximum "False" 
     .SetFixPlotMaximumValue "1" 
     .SetInverseAxialRatio "False" 
     .SetAxesType "user" 
     .SetAntennaType "unknown" 
     .Phistart "1.000000e+00", "0.000000e+00", "0.000000e+00" 
     .Thetastart "0.000000e+00", "0.000000e+00", "1.000000e+00" 
     .PolarizationVector "0.000000e+00", "1.000000e+00", "0.000000e+00" 
     .SetCoordinateSystemType "spherical" 
     .SetAutomaticCoordinateSystem "True" 
     .SetPolarizationType "Linear" 
     .SlantAngle 0.000000e+00 
     .Origin "bbox" 
     .Userorigin "0.000000e+00", "0.000000e+00", "0.000000e+00" 
     .SetUserDecouplingPlane "False" 
     .UseDecouplingPlane "False" 
     .DecouplingPlaneAxis "X" 
     .DecouplingPlanePosition "0.000000e+00" 
     .LossyGround "False" 
     .GroundEpsilon "1" 
     .GroundKappa "0" 
     .EnablePhaseCenterCalculation "False" 
     .SetPhaseCenterAngularLimit "3.000000e+01" 
     .SetPhaseCenterComponent "boresight" 
     .SetPhaseCenterPlane "both" 
     .ShowPhaseCenter "True" 
     .ClearCuts 
     .StoreSettings
End With

'@ reset mcalc defaults

'[VERSION]2021.0|30.0.1|20200813[/VERSION]
Mesh.ResetToMCalcDefaults

'@ set PBA version

'[VERSION]2021.0|30.0.1|20200813[/VERSION]
Mesh.PBAVersion "2020081321"

'@ set mesh properties (Hexahedral)

'[VERSION]2021.0|30.0.1|20200813[/VERSION]
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
     .Set "StepsPerBoxNear", "20" 
     .Set "StepsPerBoxFar", "1" 
     .Set "MaxStepNear", "0" 
     .Set "MaxStepFar", "0" 
     .Set "ModelBoxDescrNear", "maxedge" 
     .Set "ModelBoxDescrFar", "maxedge" 
     .Set "UseMaxStepAbsolute", "0" 
     .Set "GeometryRefinementSameAsNear", "0" 
     'MIN CELL 
     .Set "UseRatioLimitGeometry", "1" 
     .Set "RatioLimitGeometry", "15" 
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
     .Set "EdgeRefinementRatio", "2" 
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
     .PointAccEnhancement "0" 
     .TSTVersion "0"
	  .PBAVersion "2020081321" 
End With

