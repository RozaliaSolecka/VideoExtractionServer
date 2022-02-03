from scripts.training_effectiveness.record import Record


def IoU(record: Record, other: Record):
    xA = max(record.x_l, other.x_l)  # coordinates of overlap A = (xl, yu), B = (xr, yd)
    yA = max(record.y_u, other.y_u)
    xB = min(record.x_r, other.x_r)
    yB = min(record.y_d, other.y_d)

    area_of_overlap = max(0.0, xB - xA) * max(0.0, yB - yA)
    area_of_union = (float(record.width) * float(record.height)) + \
        (float(other.width) * float(other.height)) - \
        area_of_overlap

    if area_of_union > 0:
        return area_of_overlap / area_of_union
    else:
        return 0
