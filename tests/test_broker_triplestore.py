from emobon.brokers.triplestore import TriplestoreBroker
from emobon.udal import UDAL
from emobon.namedqueries import (
    QUERY_REGISTER,
    QueryName,
    QUERY_NAMES,
    NamedQueryInfo,
)

from emobon.result import Result
import datetime


def test_observatory_overview():
    """Test the observatory overview query."""
    broker = TriplestoreBroker()
    result = broker.execute("urn:embrc.eu:emobon:observatory-overview")
    assert isinstance(result, Result)
    assert len(result.data()) > 0
    # check if result.data() is a dict
    assert isinstance(result.data(), dict)
    # chekc if the following keys are present in the result
    # uri, observatory_id, type, countries , broadbiomes , localbiomes
    assert "uri" in result.data()
    assert "observatory_id" in result.data()
    assert "types" in result.data()
    assert "countries" in result.data()
    assert "broadbiomes" in result.data()
    assert "localbiomes" in result.data()


def test_udal_instance():
    """Test the UDAL instance."""
    udal = UDAL()
    assert isinstance(udal, UDAL)
    assert isinstance(udal.queries, dict)
    assert len(udal.queries) > 0
    assert isinstance(udal.query_names, list)
    assert len(udal.query_names) > 0
    # check if the query names are in the QUERY_NAMES
    for name in udal.query_names:
        assert name in QUERY_NAMES
        # check if the query is in the QUERY_REGISTER
        assert name in QUERY_REGISTER
        # check if the query is in the broker queries
        assert name in udal._broker.queries
        print(f"{name=}")


def test_observatory_overview_totals():
    """Test the observatory overview totals query."""
    broker = TriplestoreBroker()
    result = broker.execute("urn:embrc.eu:emobon:observatory-overview-totals")
    assert isinstance(result, Result)
    assert len(result.data()) > 0
    # check if result.data() is a dict
    assert isinstance(result.data(), dict)
    # check if the following keys are present in the result
    # uri, observatory_id, type, countries , broadbiomes , localbiomes
    # also have a count of the sampling events per observatory
    # min -max dates of the sampling events
    # number of samples

    assert "uri" in result.data()
    assert "observatory_id" in result.data()
    assert "types" in result.data()
    assert "countries" in result.data()
    assert "broadbiomes" in result.data()
    assert "localbiomes" in result.data()
    assert "sampling_events_count" in result.data()
    # should be an list of integers
    assert isinstance(result.data()["sampling_events_count"], list)
    assert all(isinstance(i, int) for i in result.data()["sampling_events_count"])
    # check if the min and max dates are present
    # should be a list of strings that are xsd:dateTime formatted
    assert "min_date" in result.data()
    assert isinstance(result.data()["min_date"], list)
    assert all(isinstance(i, datetime.date) for i in result.data()["min_date"])

    assert "max_date" in result.data()
    assert isinstance(result.data()["max_date"], list)
    assert all(isinstance(i, datetime.date) for i in result.data()["max_date"])


def test_measured_values():
    """Test the measured values query."""
    broker = TriplestoreBroker()
    result = broker.execute("urn:embrc.eu:emobon:measured-values")
    assert isinstance(result, Result)
    assert len(result.data()) > 0
    # check if result.data() is a dict
    assert isinstance(result.data(), dict)
    # check if the following keys are present in the result
    # measured_parameter, value , unit , context (dict)
    # context keys , observatory_id , sampling_event, sampling_type
    # date, position_depth, position_location , instrument_type

    assert "measured_parameter" in result.data()
    assert "value" in result.data()
    assert "unit" in result.data()
    assert "context" in result.data()
    # check if context is a dict
    assert isinstance(result.data()["context"], dict)
    # check if the following keys are present in the context
    # observatory_id , sampling_event, sampling_type
    # date, position_depth, position_location , instrument_type
    context = result.data()["context"]
    assert "observatory_id" in context
    assert "sampling_event" in context
    assert "sampling_type" in context
    assert "date" in context
    assert "position_depth" in context
    # assert "position_location" in context
    assert "instrument_type" in context


def test_measured_values_with_params():
    """Test the measured values query with params."""
    broker = TriplestoreBroker()
    result = broker.execute(
        "urn:embrc.eu:emobon:measured-values",
        {"observatory_id": ["ROSKOGO"]},
    )
    assert isinstance(result, Result)
    assert len(result.data()) > 0
    # check if result.data() is a dict
    assert isinstance(result.data(), dict)
    # check if the following keys are present in the result
    # measured_parameter, value , unit , context (dict)
    # context keys , observatory_id , sampling_event, sampling_type
    # date, position_depth, position_location , instrument_type

    assert "measured_parameter" in result.data()
    assert "value" in result.data()
    assert "unit" in result.data()
    assert "context" in result.data()
    # check if context is a dict
    assert isinstance(result.data()["context"], dict)


def test_ssu_with_params():
    """Test the SSU query with params."""
    broker = TriplestoreBroker()
    result = broker.execute(
        "urn:embrc.eu:emobon:ssu",
        {
            "abundance_lower": 10,
            "abundance_upper": 100,
        },
    )
    assert isinstance(result, Result)
    assert len(result.data()) > 0
    print(result.data())
    # check if result.data() is a dict
    assert isinstance(result.data(), dict)
    # check if the following keys are present in the result
    # ref_code, ncbi_tax_id, abundance, scientific_name, taxon_rank, taxon_id
    assert "ref_code" in result.data()
    assert "ncbi_tax_id" in result.data()
    assert "abundance" in result.data()
    assert "scientific_name" in result.data()
    assert "taxon_rank" in result.data()


def test_lsu_with_params():
    """Test the SSU query with params."""
    broker = TriplestoreBroker()
    result = broker.execute(
        "urn:embrc.eu:emobon:lsu",
        {
            "abundance_lower": 10,
            "abundance_upper": 100,
        },
    )
    assert isinstance(result, Result)
    assert len(result.data()) > 0
    print(result.data())
    # check if result.data() is a dict
    assert isinstance(result.data(), dict)
    # check if the following keys are present in the result
    # ref_code, ncbi_tax_id, abundance, scientific_name, taxon_rank, taxon_id
    assert "ref_code" in result.data()
    assert "ncbi_tax_id" in result.data()
    assert "abundance" in result.data()
    assert "scientific_name" in result.data()
    assert "taxon_rank" in result.data()


def test_observatories():
    """Test the observatories query."""
    broker = TriplestoreBroker()
    result = broker.execute("urn:embrc.eu:emobon:observatories")
    assert isinstance(result, Result)
    assert len(result.data()) > 0
    # check if result.data() is a dict
    assert isinstance(result.data(), dict)
    # check if the following keys are present in the result
    # uri, observatory_id, type, countries , broadbiomes , localbiomes
    assert "obs_id" in result.data()
    assert "country" in result.data()
    assert "env_package" in result.data()
    assert "loc_regional_mgrid" in result.data()
    assert "tot_depth_water_column" in result.data()


def test_observatories_with_params():
    broker = TriplestoreBroker()
    result = broker.execute(
        "urn:embrc.eu:emobon:observatories",
        {"loc_regional_mgrid": ["English Channel"]},
    )
    assert isinstance(result, Result)
    assert len(result.data()) > 200
    # check if result.data() is a dict
    assert isinstance(result.data(), dict)
    # check if the following keys are present in the result
    # uri, observatory_id, type, countries , broadbiomes , localbiomes
    assert "obs_id" in result.data()
    assert "country" in result.data()
    assert "env_package" in result.data()
    assert "loc_regional_mgrid" in result.data()
    assert "tot_depth_water_column" in result.data()
