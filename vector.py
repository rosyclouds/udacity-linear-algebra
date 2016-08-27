import math
from decimal import Decimal,getcontext

getcontext().prec=30
round_prec=10

class VectorIterCoordinate:
    def __init__(self,vector):
        self.vector=vector
        self.index=0

    def __next__(self):
        if self.index>=len(self.vector.coordinates):
            raise StopIteration
        else:
            tmp=self.vector.coordinates[self.index]
            self.index+=1
            return tmp

class Vector:
    def __init__(self,coordinates):
        try:            
            if not coordinates:
                raise ValueError
            self.coordinates=tuple(Decimal(component) for component in coordinates)
            self.dimension=len(self.coordinates)
        except ValueError:
            raise ValueError('The coordinates must be nonempty')
        except TypeError:
            raise TypeError('The coordinates must be an iterable')
        
          
    def __add__(self,other):
        try:
            if self.dimension!=other.dimension:
                raise Exception('Vector addtion valid for two vectors under same dimension')
            return Vector(x+y for x,y in zip(self.coordinates,other.coordinates))
        except AttributeError:
            raise Exception('Vector addtion valid for two vectors')

    def __sub__(self,other):
        return self+(-1*other)

    def scalar_mul(self,number):
            return Vector(round((x*number),round_prec) for x in self.coordinates)    

    def dot_product(self,other):
            if self.dimension!=other.dimension:
                raise Exception('Vector dot product valid for two vectors under same dimension')
            return sum(x*y for x,y in zip(self.coordinates,other.coordinates))

    def __mul__(self,other):
        if isinstance(other,float):
            other=Decimal(other)
        mul_dict={int:self.scalar_mul,Decimal:self.scalar_mul,Vector:self.dot_product}
        return mul_dict[other.__class__](other)

    @property
    def magnitude(self,):
        return math.sqrt(self*self)

    def normalized(self,):
        try:
            return self*(1/self.magnitude)
        except ZeroDivisionError:
            raise Exception('Can\'t normalize the zero vector')
            
    def angle_with(self,other,in_degrees=False):
        try:
            u1=self.normalized()
            u2=other.normalized()
            angle_in_radians=math.acos(u1*u2)

            if in_degrees:
                degrees_per_radian= 180 /math.pi
                return angle_in_radians*degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e)=='Can\'t normalize the zero vector':
                raise Exception('Cannot compute an angle with the zero vector')
            if str(e)=='Vector dot product valid for two vectors under same dimension':
                raise Exception('Angle Between Two Vectors need in the same dimension')
            else:
                raise e  

    def is_zero(self,tolerance=1e-10):
        return self.magnitude<tolerance

    def is_orthogonal_to(self,other,tolerance=1e-10):
        return abs(self*other)<tolerance

    def is_parallel_to(self,other):
        return (self.is_zero() or
                other.is_zero() or
                self.angle_with(other)==0 or
                self.angle_with(other)==math.pi)
        
    def project_onto(self,other):
        try:
            unit_other=other.normalized()
            return (self*unit_other)*unit_other
        except Exception as e:
            if str(e)=='Can\'t normalize the zero vector':
                raise Exception('Can\'t project onto the zero vector')
            else:
                raise e


    def orthogonal_onto(self,other):
        return self-self.project_onto(other)

    
    def cross_product(self,other):
        try:
            a_1,a_2,a_3=self.coordinates
            b_1,b_2,b_3=other.coordinates
            v1=a_2*b_3-a_3*b_2
            v2=a_3*b_1-a_1*b_3
            v3=a_1*b_2-b_2*a_1
            return Vector((v1,v2,v3))
        except ValueError:
            raise Exception('Cross Product defined only in three dimension vector')


    def area_of_span_parallelogram(self,other):
        cross_product=self.cross_product(other)
        return cross_product.magnitude


    def area_of_span_triangle(self,other):
        return 0.5*self.area_of_span_parallelogram(other)

    def __iter__(self):
        return VectorIterCoordinate(self)

    def __getitem__(self,index):
        return self.coordinates[index]
    
    
    def __eq__(self,other):
        return self.coordinates==other.coordinates
        
    def __str__(self):
        return 'vertor: {}'.format(self.coordinates)

    __repr__=__str__
        
    __rmul__=__mul__
