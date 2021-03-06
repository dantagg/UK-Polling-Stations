from data_collection.management.commands import BaseXpressDemocracyClubCsvImporter


class Command(BaseXpressDemocracyClubCsvImporter):
    council_id = "E07000216"
    addresses_name = "parl.2019-12-12/Version 3/merged.tsv"
    stations_name = "parl.2019-12-12/Version 3/merged.tsv"
    elections = ["parl.2019-12-12"]
    csv_delimiter = "\t"
    allow_station_point_from_postcode = False

    def address_record_to_dict(self, record):
        rec = super().address_record_to_dict(record)
        uprn = record.property_urn.strip().lstrip("0")
        if uprn == "100062163595":
            return None

        if uprn in [
            "200001286366",  # GU50LG -> GU50LH : The Old Cottage, Grafham, Bramley, Guildford, Surrey
            "200003086280",  # GU84BH -> GU84BX : Gorebridge House, Loxhill, Godalming, Surrey
            "100061616798",  # GU85UJ -> GU85LA : Brook Grange, Haslemere Road, Brook, Godalming, Surrey
            "10013894366",  # GU99JT -> GU97JT : 5 Stoke House, 17 St James Terrace, Farnham, Surrey
            "100062163296",  # GU71SX -> GU71XS : 10 Lawnwood Court, Catteshall Lane, Godalming, Surrey
            "100061625643",  # GU50TJ -> GU50TP : Thanescroft, Lords Hill Common, Shamley Green, Guildford, Surrey
            "200001294523",  # GU50LG -> GU50LH : Rushett Farm Cottage, Rushett Common, Bramley, Guildford, Surrey
            "200001537439",  # GU50SU -> GU68QY : Willinghurst Lodge, Willinghurst Estate, Shamley Green, Guildford, Surrey
        ]:
            rec["accept_suggestion"] = True

        if uprn in [
            "10013894393",  # GU103QY -> GU98DR : 3 Tattingstone Close, Lower Bourne, Farnham, Surrey
            "100062339874",  # GU97DR -> GU272AJ : Merriott House, 26 West Street, Farnham, Surrey
            "100062339873",  # GU97DR -> GU272AH : 24 West Street, Farnham, Surrey
            "100062339881",  # GU104BT -> GU272HG : 27 High Street, Rowledge, Farnham, Surrey
            "200001536207",  # GU103BS -> GU102AZ : Keepers Cottage Pierrepont Farm, Priory Lane, Frensham, Farnham, Surrey
        ]:
            rec["accept_suggestion"] = False

        return rec
