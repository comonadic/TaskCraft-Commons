import rhino3dm as rh
def build(parts,out):
    out.mkdir(parents=True,exist_ok=True);model=rh.File3dm();model.Settings.ModelUnitSystem=rh.UnitSystem.Millimeters;obj=[];offset=0
    for p in parts:
        x,y,z,dx,dy,dz=p['box'];v=[(x,y,z),(x+dx,y,z),(x+dx,y+dy,z),(x,y+dy,z),(x,y,z+dz),(x+dx,y,z+dz),(x+dx,y+dy,z+dz),(x,y+dy,z+dz)];faces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)];mesh=rh.Mesh()
        for point in v:mesh.Vertices.Add(*point)
        for face in faces:mesh.Faces.AddFace(*face)
        mesh.Normals.ComputeNormals();attrs=rh.ObjectAttributes();attrs.Name=p['id'];model.Objects.AddMesh(mesh,attrs)
        obj.append('o '+p['id']);obj.extend('v '+' '.join(str(n) for n in pt) for pt in v);obj.extend('f '+' '.join(str(offset+i+1) for i in f) for f in faces);offset+=len(v)
    model.Write(str(out/'model.3dm'),8);(out/'model.obj').write_text('\n'.join(obj)+'\n')
