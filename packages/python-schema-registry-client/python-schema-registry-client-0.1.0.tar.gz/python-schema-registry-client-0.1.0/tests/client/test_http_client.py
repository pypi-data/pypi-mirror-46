import pytest
import requests

from avro.schema import SchemaFromJSONData

from schema_registry.client import SchemaRegistryClient, load

from tests.client import data_gen


def assertLatest(self, meta_tuple, sid, schema, version):
    self.assertNotEqual(sid, -1)
    self.assertNotEqual(version, -1)
    self.assertEqual(meta_tuple[0], sid)
    self.assertEqual(meta_tuple[1], schema)
    self.assertEqual(meta_tuple[2], version)


def test_register(client):
    parsed = load.loads(data_gen.BASIC_SCHEMA)
    schema_id = client.register("test", parsed)

    assert schema_id > 0
    assert len(client.id_to_schema) == 1


def test_register_json_data(client, user_schema):
    schema_id = client.register("test", user_schema)
    assert schema_id > 0


def test_register_with_custom_headers(client, country_schema):
    headers = {"custom-serialization": "application/x-avro-json"}
    schema_id = client.register("test", country_schema, headers=headers)
    assert schema_id > 0


def test_multi_subject_register(client):
    parsed = load.loads(data_gen.BASIC_SCHEMA)
    schema_id = client.register("test", parsed)
    assert schema_id > 0

    # register again under different subject
    dupe_id = client.register("other", parsed)
    assert schema_id == dupe_id
    assert len(client.id_to_schema) == 1


def test_dupe_register(client):
    parsed = load.loads(data_gen.BASIC_SCHEMA)
    subject = "test"
    schema_id = client.register(subject, parsed)

    assert schema_id > 0
    latest = client.get_schema(subject)

    # register again under same subject
    dupe_id = client.register(subject, parsed)
    assert schema_id == dupe_id

    dupe_latest = client.get_schema(subject)
    assert latest == dupe_latest


def test_getters(client):
    parsed = load.loads(data_gen.BASIC_SCHEMA)
    subject = "test"
    version = client.check_version(subject, parsed)
    assert version is None

    schema = client.get_by_id(1)
    assert schema is None

    latest = client.get_schema(subject)
    assert latest == (None, None, None, None)

    # register
    schema_id = client.register(subject, parsed)
    schema = client.get_schema(subject, schema_id)
    assert schema is not None

    latest = client.get_schema(subject)
    version = client.check_version(subject, parsed)
    fetched = client.get_by_id(schema_id)

    assert fetched == parsed


def test_multi_register(client):
    basic = load.loads(data_gen.BASIC_SCHEMA)
    adv = load.loads(data_gen.ADVANCED_SCHEMA)
    subject = "test"

    id1 = client.register(subject, basic)
    latest_schema_1 = client.get_schema(subject)
    client.check_version(subject, basic)

    id2 = client.register(subject, adv)
    latest_schema_2 = client.get_schema(subject)
    client.check_version(subject, adv)

    assert id1 != id2
    assert latest_schema_1 != latest_schema_2
    # ensure version is higher
    assert latest_schema_1.version < latest_schema_2.version

    client.register(subject, basic)
    latest_schema_3 = client.get_schema(subject)
    # latest should not change with a re-reg
    assert latest_schema_2 == latest_schema_3


def test_context(client):
    with client as c:
        parsed = load.loads(data_gen.BASIC_SCHEMA)
        schema_id = c.register("test", parsed)
        assert schema_id > 0
        assert len(c.id_to_schema) == 1


def test_cert_no_key():
    with pytest.raises(ValueError):
        SchemaRegistryClient(
            url="https://127.0.0.1:65534", cert_location="/path/to/cert"
        )


def test_cert_with_key():
    client = SchemaRegistryClient(
        url="https://127.0.0.1:65534",
        cert_location="/path/to/cert",
        key_location="/path/to/key",
    )

    assert ("/path/to/cert", "/path/to/key") == client._session.cert


def test_custom_headers():
    extra_headers = {"custom-serialization": "application/x-avro-json"}

    client = SchemaRegistryClient(
        url="https://127.0.0.1:65534", extra_headers=extra_headers
    )
    assert extra_headers == client.extra_headers


def test_override_headers(client, user_schema, mocker):
    extra_headers = {"custom-serialization": "application/x-avro-json"}
    client = SchemaRegistryClient(
        "https://127.0.0.1:65534", extra_headers=extra_headers
    )

    assert (
        client.prepare_headers().get("custom-serialization")
        == "application/x-avro-json"
    )

    class Response:
        def __init__(self, status_code, content=None):
            self.status_code = status_code

            if content is None:
                content = {}

            self.content = content

        def json(self):
            return self.content

    subject = "test"
    override_header = {"custom-serialization": "application/avro"}

    request_patch = mocker.patch.object(
        requests.sessions.Session,
        "request",
        return_value=Response(200, content={"id": 1}),
    )
    client.register(subject, user_schema, headers=override_header)

    prepare_headers = client.prepare_headers(body="1")
    prepare_headers["custom-serialization"] = "application/avro"

    request_patch.assert_called_once_with(
        "POST", mocker.ANY, headers=prepare_headers, json=mocker.ANY
    )


def test_cert_path():
    client = SchemaRegistryClient(
        url="https://127.0.0.1:65534", ca_location="/path/to/ca"
    )

    assert "/path/to/ca" == client._session.verify


def test_init_with_dict():
    client = SchemaRegistryClient(
        {
            "url": "https://127.0.0.1:65534",
            "ssl.certificate.location": "/path/to/cert",
            "ssl.key.location": "/path/to/key",
        }
    )
    assert "https://127.0.0.1:65534" == client.url


def test_empty_url():
    with pytest.raises(ValueError):
        SchemaRegistryClient({"url": ""})


def test_invalid_type_url():
    with pytest.raises(TypeError):
        SchemaRegistryClient(url=1)


def test_invalid_type_url_dict():
    with pytest.raises(TypeError):
        SchemaRegistryClient({"url": 1})


def test_invalid_url():
    with pytest.raises(ValueError):
        SchemaRegistryClient({"url": "example.com:65534"})


def test_basic_auth_url():
    client = SchemaRegistryClient(
        {"url": "https://user_url:secret_url@127.0.0.1:65534"}
    )

    assert ("user_url", "secret_url") == client._session.auth


def test_basic_auth_userinfo():
    client = SchemaRegistryClient(
        {
            "url": "https://user_url:secret_url@127.0.0.1:65534",
            "basic.auth.credentials.source": "user_info",
            "basic.auth.user.info": "user_userinfo:secret_userinfo",
        }
    )
    assert ("user_userinfo", "secret_userinfo") == client._session.auth


def test_basic_auth_sasl_inherit():
    client = SchemaRegistryClient(
        {
            "url": "https://user_url:secret_url@127.0.0.1:65534",
            "basic.auth.credentials.source": "SASL_INHERIT",
            "sasl.mechanism": "PLAIN",
            "sasl.username": "user_sasl",
            "sasl.password": "secret_sasl",
        }
    )
    assert ("user_sasl", "secret_sasl") == client._session.auth


def test_basic_auth_invalid():
    with pytest.raises(ValueError):
        SchemaRegistryClient(
            {
                "url": "https://user_url:secret_url@127.0.0.1:65534",
                "basic.auth.credentials.source": "VAULT",
            }
        )


def test_invalid_conf():
    with pytest.raises(ValueError):
        SchemaRegistryClient(
            {
                "url": "https://user_url:secret_url@127.0.0.1:65534",
                "basic.auth.credentials.source": "SASL_INHERIT",
                "sasl.username": "user_sasl",
                "sasl.password": "secret_sasl",
                "invalid.conf": 1,
                "invalid.conf2": 2,
            }
        )
