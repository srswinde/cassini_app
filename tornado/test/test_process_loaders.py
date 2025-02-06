import pytest
from datetime import datetime, timedelta
from api.process_loaders import get_day
from database.models import hole_camera

EXPECTED_EXCEPTION = ValueError 

def test_get_day_future_date():
    """Test that get_day raises an exception when the date is in the future.
    """
    # Create a date that is in the futurecd 
    future_date = datetime.now() + timedelta(days=1)

    # Check that calling get_day with a future date raises the expected exception
    with pytest.raises(EXPECTED_EXCEPTION):
        get_day(hole_camera, date=future_date)

def test_example():
    """Sanity check on the test suite
    """
    assert 1 == 1