# encoding: utf-8

import StringIO
import os
import uuid
import datetime
import OpenSSL.crypto

from lxml import etree as etree_
from documentoCedible import DocumentoCedible

import signxml
from signxml import XMLSigner, XMLVerifier
from signxml.util import long_to_bytes, ensure_str, b64encode
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def document_export_xml(document, validate_schema=True, schemas_path=None, certificate=None):
    # type: (DocumentoCedible, bool, basestring, tuple[any, basestring]) -> basestring
    """
        Genera el XML del documento firmado.

    :return: Xml string.
    :param document: Documento cedible..
    :param validate_schema: Validar el esquema?
    :param schemas_path: Directorio con los esquemas.
    :param certificate: Tupla con el data y la contrasena del certificado para la firma.
    :return:
    """

    document.Documento.ID = 'DOC_{}'.format(str(uuid.uuid4()))
    document.Documento.TmstFirma = datetime.datetime.now()

    string_buffer = StringIO.StringIO()
    document.export(string_buffer, 0, pretty_print=True)

    xml_str = string_buffer.getvalue()
    xml_to_validate = xml_str.replace('<SiiDte:DocumentoCedible>',
                                      '<SiiDte:DocumentoCedible version="1.0" xmlns="http://www.sii.cl/SiiDte">')
    xml_to_validate = xml_to_validate.replace('SiiDte:', '')

    if certificate is not None and isinstance(certificate, tuple):
        certificate_data = certificate[0]
        certificate_pass = certificate[1]
        xml_to_validate = _sign_document(xml_to_validate, certificate_data, certificate_pass)

    if validate_schema:
        try:
            schemas_path = schemas_path \
                          or os.path.join(os.path.dirname(__file__), '..', 'schemas')

            schema_file_name = os.path.join(schemas_path, 'DocumentoCedible_v10.xsd')
            schema_file = open(schema_file_name, 'r')
            schema_root = etree_.parse(schema_file)
            schema = etree_.XMLSchema(schema_root)

            doc = etree_.parse(StringIO.StringIO(xml_to_validate))
            schema.assertValid(doc)
        except etree_.DocumentInvalid as ex:
            no_throw = len(ex.args) == 1 and 'Signature' in ex.args[0]
            if not no_throw:
                raise Exception(str(ex))

    return xml_to_validate


def _sign_document(xml_str, certificate, password):
    # type: (basestring, any, basestring) -> basestring
    """

    :return:
    :param xml_str:
    :param certificate:
    :param password:
    :return:
    """
    xml = etree_.XML(xml_str)

    namespaces = {'x': 'http://www.sii.cl/SiiDte'}
    document_node = xml.xpath('//x:Documento', namespaces=namespaces)[0]

    cert_key, cert_cert = _read_certificate(certificate, password)

    c14n_algorithm = 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'
    signer = XMLSigner(method=signxml.methods.detached,
                       signature_algorithm='rsa-sha1', digest_algorithm='sha1',
                       c14n_algorithm=c14n_algorithm)
    signature_node = signer.sign(document_node, key=cert_key, cert=cert_cert)

    # Add Transform
    signature_namespaces = {'s': 'http://www.w3.org/2000/09/xmldsig#'}
    reference_node = signature_node.xpath('//s:SignedInfo/s:Reference', namespaces=signature_namespaces)
    if len(reference_node) > 0:
        transforms = reference_node[0].xpath('//s:Transforms', namespaces=signature_namespaces)
        if len(transforms) == 0:
            transforms = _insert_node_first(reference_node[0], '{http://www.w3.org/2000/09/xmldsig#}Transforms')
            etree_.SubElement(transforms, '{http://www.w3.org/2000/09/xmldsig#}Transform', Algorithm=c14n_algorithm)

    # Add KeyValue
    key_info_element = signature_node.xpath('//s:KeyInfo', namespaces=signature_namespaces)[0]
    if len(key_info_element.xpath('//s:KeyValue', namespaces=signature_namespaces)) == 0:
        key = load_pem_private_key(cert_key, password=None, backend=default_backend())
        key_value = _insert_node_first(key_info_element, '{http://www.w3.org/2000/09/xmldsig#}KeyValue')
        rsa_key_value = etree_.SubElement(key_value, '{http://www.w3.org/2000/09/xmldsig#}RSAKeyValue')
        modulus = etree_.SubElement(rsa_key_value, '{http://www.w3.org/2000/09/xmldsig#}Modulus')
        modulus.text = ensure_str(b64encode(long_to_bytes(key.public_key().public_numbers().n)))
        exponent = etree_.SubElement(rsa_key_value, '{http://www.w3.org/2000/09/xmldsig#}Exponent')
        exponent.text = ensure_str(b64encode(long_to_bytes(key.public_key().public_numbers().e)))

    parent = document_node.getparent()
    parent.append(signature_node)

    # verified_data = XMLVerifier().verify(xml, x509_cert=cert_cert).signed_xml

    xml_str = etree_.tostring(xml, pretty_print=True, xml_declaration=True, encoding='iso-8859-1')
    xml_str = xml_str.replace('ds:', '').replace('xmlns:ds=', 'xmlns=')

    return xml_str


def _insert_node_first(parent, nodeName):
    """

    :param parent:
    :param nodeName:
    :return:
    """
    # Remove children
    child = []
    for c in parent:
        child.append(c)
    for c in child:
        parent.remove(c)

    # Create new node
    node = etree_.SubElement(parent, nodeName)

    # Append old children
    for c in child:
        parent.append(c)

    return node


def _read_certificate(certificate, password):
    """

    :param certificate:
    :param password:
    :return:
    """
    p12 = OpenSSL.crypto.load_pkcs12(certificate, passphrase=password)

    pk = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey())
    cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate())

    return pk, cert
