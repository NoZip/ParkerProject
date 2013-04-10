import numpy

def Vector3D(*args, **kwargs):
    if args and len(args) == 3:
        return numpy.array(args)
    elif 'x' in kwargs and 'y' in kwargs and 'z' in kwargs:
        return numpy.array([kwargs['x'], kwargs['y'], kwargs['z']])

if __name__ == "__main__":
    v1 = Vector3D(1,2,3)
    v2 = Vector3D(x=2, y=8, z=7)
    
    print(v1)
    print(v2)
    print(v1 + v2)
