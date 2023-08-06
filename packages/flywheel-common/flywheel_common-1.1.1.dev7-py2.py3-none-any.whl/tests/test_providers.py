from marshmallow import exceptions
from mock import patch
import datetime
import pytest

from flywheel_common.errors import ValidationError
from flywheel_common.providers import ProviderClass
from flywheel_common.providers.creds import Creds
from flywheel_common.providers.provider import BaseProvider
from flywheel_common.providers.storage.base import BaseStorageProvider
from flywheel_common.providers.compute.base import BaseComputeProvider


# === Model Tests ===
def test_creds():

    cred_test = Creds(
        provider_class='test',
        provider_type='anything',
        provider_label='Test creds',
        config=None)

    assert cred_test.provider_class == 'test'
    assert cred_test.provider_type == 'anything'
    assert cred_test.label == 'Test creds'

    # No schema
    with pytest.raises(ValueError):
        cred_test.validate()

def test_provider():

    provider_test = BaseProvider(
        provider_class='test',
        provider_type='anything',
        provider_label='Test provider',
        config=None,
        creds=None)

    assert provider_test.provider_class == 'test'
    assert provider_test.provider_type == 'anything'
    assert provider_test.label == 'Test provider'

    # No schema
    with pytest.raises(ValueError):
        provider_test.validate()

def test_storage_provider(mocker):

    mocker.patch('flywheel_common.providers.storage.base.create_flywheel_fs', return_value={'storage': 'test'})
    provider_test = BaseStorageProvider(
        provider_class=ProviderClass.storage.value,
        provider_type='local',
        provider_label='Test local provider',
        config={'path': '/var/'},
        creds=None)

    assert provider_test.label == 'Test local provider'
    assert provider_test.provider_class == ProviderClass.storage.value
    assert provider_test.provider_type == 'local'
    assert provider_test.storage_plugin == {'storage': 'test'}

    # No schema
    with pytest.raises(ValueError):
        provider_test.validate()

def test_compute_provider(mocker):
    """Test validation on all the required fields for base compute"""

    origin = { 'type': 'user', 'id': 'user@test.com' }
    # Dont use defaults to confirm they are set in the model correctly
    config = {
        'cloud_queue_threshold': 5,
        'cloud_max_compute': 6,
        'cloud_machine_type': 'test',
        'cloud_disk_size': 7,
        'cloud_swap_size': 8,
        'cloud_preemptible': 9
    }

    provider_test = BaseComputeProvider(
        provider_class=ProviderClass.storage.value,
        provider_type='local',
        provider_label='Test local provider',
        config=config,
        creds=None)
    provider_test.origin = origin
    provider_test.created = provider_test.modified = datetime.datetime.now()

    assert provider_test.label == 'Test local provider'
    assert provider_test.provider_class == ProviderClass.storage.value
    assert provider_test.provider_type == 'local'
    assert provider_test.config['cloud_queue_threshold'] == 5
    assert provider_test.config['cloud_max_compute'] == 6
    assert provider_test.config['cloud_machine_type'] == 'test'
    assert provider_test.config['cloud_disk_size'] == 7
    assert provider_test.config['cloud_swap_size'] == 8
    assert provider_test.config['cloud_preemptible'] == 9

    # No errors should be thrown here
    provider_test.validate()

    provider_test.config['cloud_queue_threshold'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_queue_threshold'] = 'Strings not allowed'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_queue_threshold'] = 5

    provider_test.config['cloud_max_compute'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_max_compute'] = 'Strings not allowed'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_max_compute'] = 6

    provider_test.config['cloud_machine_type'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_machine_type'] = 999
    # Numbers are convered to strings so this is valid
    provider_test.validate()
    provider_test.config['cloud_machine_type'] = 'test'

    provider_test.config['cloud_disk_size'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_disk_size'] = 'Strings not allowed'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_disk_size'] = 7

    provider_test.config['cloud_swap_size'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_swap_size'] = 'Strings not allowed'
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_swap_size'] = 8

    provider_test.config['cloud_preemptible'] = None
    with pytest.raises(ValidationError):
        provider_test.validate()
    provider_test.config['cloud_preemptible'] = 'String'
    # It converts string to a bool value on validate
    provider_test.validate()
    provider_test.config['cloud_preemptible'] = 333
    # Converts number to bool on validate as well
    provider_test.validate()
    provider_test.config['cloud_preemptible'] = True
