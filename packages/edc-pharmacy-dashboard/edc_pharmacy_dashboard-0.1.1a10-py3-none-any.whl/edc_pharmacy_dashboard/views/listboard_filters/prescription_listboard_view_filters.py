from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters


class PrescriptionListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(name="all", position=0, label="All", lookup={})

    missed = ListboardFilter(
        name="control", position=10, label="Control Arm", lookup={"rx": True}
    )

    previous = ListboardFilter(
        name="single_dose",
        label="Single Dose",
        position=20,
        lookup={"singledose": True},
    )
