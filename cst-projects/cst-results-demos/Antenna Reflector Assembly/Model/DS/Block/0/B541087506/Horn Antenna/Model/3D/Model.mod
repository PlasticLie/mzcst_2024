'# MWS Version: Version 2024.0 - Jul 09 2023 - ACIS 33.0.1 -

'# length = mm
'# frequency = GHz
'# time = ns
'# frequency range: fmin = 4 fmax = 5
'# created = '[VERSION]2017.0|26.0.1|20161127[/VERSION]


'@ new component: component1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Component 
.New "component1"
End With

'@ define brick: component1:solid1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Brick 
.Reset
.Name "solid1"
.Component "component1"
.Material "PEC"
.Xrange "-waveguide_width/2", "waveguide_width/2"
.Yrange "-waveguide_height/2", "waveguide_height/2"
.Zrange "0", "6"
.Create
End With

'@ pick face

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Pick
.PickFaceFromId "component1:solid1", "1"
End With

'@ define extrude: component1:solid2

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Extrude
.Name "solid2"
.Component "component1"
.Material "PEC"
.Mode "Picks"
.Height "horn_length"
.Twist "0.0"
.Taper "taper_angle"
.UsePicksForHeight "False"
.DeleteBaseFaceSolid "False"
.ClearPickedFace "True"
.Create
End With

'@ boolean add shapes: component1:solid1, component1:solid2

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Solid
.Add "component1:solid1", "component1:solid2"
End With

'@ pick face

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Pick
.PickFaceFromId "component1:solid1", "5"
End With

'@ pick face

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Pick
.PickFaceFromId "component1:solid1", "8"
End With

'@ shell object: component1:solid1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Solid
.AdvancedShell "component1:solid1", "Outside", "wall_thickness"
End With

'@ pick end point

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Pick
.PickEndpointFromId "component1:solid1", "16"
End With

'@ pick end point

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Pick
.PickEndpointFromId "component1:solid1", "15"
End With

'@ pick end point

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Pick
.PickEndpointFromId "component1:solid1", "13"
End With

'@ define port: 1

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Port 
.Reset 
.PortNumber "1"
.NumberOfModes "1"
.AdjustPolarization False 
.PolarizationAngle "0.0"
.ReferencePlaneDistance "0"
.TextSize "50"
.Coordinates "Picks"
.Orientation "zmin"
.PortOnBound "True"
.ClipPickedPortToBound "False"
.Create 
End With

'@ clear picks

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Pick
.ClearAllPicks
End With

'@ define units

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Units 
.Geometry "mm"
.Frequency "GHz"
.Time "ns"
End With

'@ define frequency range

'[VERSION]2017.0|26.0.1|20161205[/VERSION]
Solver.FrequencyRange "4", "5"

'@ define background

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With Background 
.Reset 
.Type "Normal"
.Epsilon "1.0"
.Mu "1.0"
.ThermalType "Normal"
.ThermalConductivity "0.0"
.XminSpace "0.0"
.XmaxSpace "0.0"
.YminSpace "0.0"
.YmaxSpace "0.0"
.ZminSpace "0.0"
.ZmaxSpace "1.5*horn_length"
.ApplyInAllDirections "False"
End With

'@ define boundaries

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
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
.Zsymmetry "none"
End With

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

'@ switch bounding box

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
Plot.DrawBox "True"

'@ switch working plane

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
Plot.DrawWorkplane "false"

'@ set mesh properties (Hexahedral)

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
With MeshSettings 
     .SetMeshType "Hex" 
     .Set "StepsPerWaveNear", "10" 
End With

'@ change solver type

'[VERSION]2017.0|26.0.1|20161127[/VERSION]
ChangeSolverType "HF Time Domain"

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

