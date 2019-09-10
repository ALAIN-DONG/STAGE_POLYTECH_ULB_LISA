from pyntcloud import PyntCloud


# filtre_ROR(point, k = int, r = float)
# Radius Outlier Removal Filter,the filter will look for the required number of neighboors inside that sphere.
# k is the number of neighbors that will be used to compute the filter
# r is the radius of the sphere with center on each point.

# filtre_SOR(point, k = int, z_max = float)
# Statistical Outlier Removal Filter
# k is the number of neighbors that will be used to compute the filter.
# z_max is the maximum Z score which determines if the point is an outlier.

def filtre_SOR(point, k = 10, z_max = 5):
    ##  Statistical Outlier Removal
    pointss = PyntCloud(points = point)
    kdtree_ids = pointss.add_structure("kdtree", leafsize = 16)
    new_filtre = pointss.get_filter("SOR", kdtree_id=kdtree_ids, and_apply=False, k = k, z_max = z_max)
    return new_filtre

def filtre_ROR(point, k = 10, r = 5):
    ##  Statistical Outlier Removal
    pointss = PyntCloud(points = point)
    kdtree_ids = pointss.add_structure("kdtree", leafsize = 16)
    new_filtre = pointss.get_filter("ROR", kdtree_id = kdtree_ids, and_apply=False, k = k, r = r)
    return new_filtre

