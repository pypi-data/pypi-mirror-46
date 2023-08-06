#!/usr/bin/env python

#
# Generated Mon Oct 22 10:48:26 2018 by generateDS.py version 2.29.24.
# Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 12:01:12)  [GCC 4.2.1 (Apple Inc. build 5666) (dot 3)]
#
# Command line options:
#   ('-o', 'classes/documentoCedible.py')
#   ('-s', 'classes/documentoCedibleSubs.py')
#   ('--super', 'DocumentCedible')
#   ('-f', '')
#   ('--no-namespace-defs', '')
#
# Command line arguments:
#   schemas/DocumentoCedible_v10.xsd
#
# Command line:
#   /Users/josfh/virtualenvs/fc-cedibledocs-py27/bin/generateDS -o "classes/documentoCedible.py" -s "classes/documentoCedibleSubs.py" --super="DocumentCedible" -f --no-namespace-defs schemas/DocumentoCedible_v10.xsd
#
# Current working directory (os.getcwd()):
#   cediblessdk
#

import sys
from lxml import etree as etree_

import DocumentCedible as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = ''

#
# Data representation classes
#


class DocumentoCedibleSub(supermod.DocumentoCedible):
    def __init__(self, version=1.0, Documento=None, Signature=None):
        super(DocumentoCedibleSub, self).__init__(version, Documento, Signature, )
supermod.DocumentoCedible.subclass = DocumentoCedibleSub
# end class DocumentoCedibleSub


class SignatureTypeSub(supermod.SignatureType):
    def __init__(self, SignedInfo=None, SignatureValue=None, KeyInfo=None):
        super(SignatureTypeSub, self).__init__(SignedInfo, SignatureValue, KeyInfo, )
supermod.SignatureType.subclass = SignatureTypeSub
# end class SignatureTypeSub


class DocumentoTypeSub(supermod.DocumentoType):
    def __init__(self, ID=None, Encabezado=None, Detalle=None, SubTotInfo=None, DscRcgGlobal=None, Referencia=None, TmstFirma=None):
        super(DocumentoTypeSub, self).__init__(ID, Encabezado, Detalle, SubTotInfo, DscRcgGlobal, Referencia, TmstFirma, )
supermod.DocumentoType.subclass = DocumentoTypeSub
# end class DocumentoTypeSub


class EncabezadoTypeSub(supermod.EncabezadoType):
    def __init__(self, IdDoc=None, Emisor=None, Receptor=None, Totales=None, OtraMoneda=None):
        super(EncabezadoTypeSub, self).__init__(IdDoc, Emisor, Receptor, Totales, OtraMoneda, )
supermod.EncabezadoType.subclass = EncabezadoTypeSub
# end class EncabezadoTypeSub


class IdDocTypeSub(supermod.IdDocType):
    def __init__(self, TipoDTE=None, Folio=None, FchEmis=None, IndNoRebaja=None, TipoDespacho=None, IndTraslado=None, TpoImpresion=None, IndServicio=None, MntBruto=None, TpoTranCompra=None, TpoTranVenta=None, FmaPago=None, FmaPagExp=None, FchCancel=None, MntCancel=None, SaldoInsol=None, MntPagos=None, PeriodoDesde=None, PeriodoHasta=None, MedioPago=None, TpoCtaPago=None, NumCtaPago=None, BcoPago=None, TermPagoCdg=None, TermPagoGlosa=None, TermPagoDias=None, FchVenc=None):
        super(IdDocTypeSub, self).__init__(TipoDTE, Folio, FchEmis, IndNoRebaja, TipoDespacho, IndTraslado, TpoImpresion, IndServicio, MntBruto, TpoTranCompra, TpoTranVenta, FmaPago, FmaPagExp, FchCancel, MntCancel, SaldoInsol, MntPagos, PeriodoDesde, PeriodoHasta, MedioPago, TpoCtaPago, NumCtaPago, BcoPago, TermPagoCdg, TermPagoGlosa, TermPagoDias, FchVenc, )
supermod.IdDocType.subclass = IdDocTypeSub
# end class IdDocTypeSub


class MntPagosTypeSub(supermod.MntPagosType):
    def __init__(self, FchPago=None, MntPago=None, GlosaPagos=None):
        super(MntPagosTypeSub, self).__init__(FchPago, MntPago, GlosaPagos, )
supermod.MntPagosType.subclass = MntPagosTypeSub
# end class MntPagosTypeSub


class EmisorTypeSub(supermod.EmisorType):
    def __init__(self, RUTEmisor=None, RznSoc=None, GiroEmis=None, Telefono=None, CorreoEmisor=None, Acteco=None, GuiaExport=None, Sucursal=None, CdgSIISucur=None, DirOrigen=None, CmnaOrigen=None, CiudadOrigen=None, CdgVendedor=None, IdAdicEmisor=None):
        super(EmisorTypeSub, self).__init__(RUTEmisor, RznSoc, GiroEmis, Telefono, CorreoEmisor, Acteco, GuiaExport, Sucursal, CdgSIISucur, DirOrigen, CmnaOrigen, CiudadOrigen, CdgVendedor, IdAdicEmisor, )
supermod.EmisorType.subclass = EmisorTypeSub
# end class EmisorTypeSub


class GuiaExportTypeSub(supermod.GuiaExportType):
    def __init__(self, CdgTraslado=None, FolioAut=None, FchAut=None):
        super(GuiaExportTypeSub, self).__init__(CdgTraslado, FolioAut, FchAut, )
supermod.GuiaExportType.subclass = GuiaExportTypeSub
# end class GuiaExportTypeSub


class ReceptorTypeSub(supermod.ReceptorType):
    def __init__(self, RUTRecep=None, CdgIntRecep=None, RznSocRecep=None, Extranjero=None, GiroRecep=None, Contacto=None, CorreoRecep=None, DirRecep=None, CmnaRecep=None, CiudadRecep=None, DirPostal=None, CmnaPostal=None, CiudadPostal=None):
        super(ReceptorTypeSub, self).__init__(RUTRecep, CdgIntRecep, RznSocRecep, Extranjero, GiroRecep, Contacto, CorreoRecep, DirRecep, CmnaRecep, CiudadRecep, DirPostal, CmnaPostal, CiudadPostal, )
supermod.ReceptorType.subclass = ReceptorTypeSub
# end class ReceptorTypeSub


class ExtranjeroTypeSub(supermod.ExtranjeroType):
    def __init__(self, NumId=None, Nacionalidad=None):
        super(ExtranjeroTypeSub, self).__init__(NumId, Nacionalidad, )
supermod.ExtranjeroType.subclass = ExtranjeroTypeSub
# end class ExtranjeroTypeSub


class TotalesTypeSub(supermod.TotalesType):
    def __init__(self, MntNeto=None, MntExe=None, MntBase=None, MntMargenCom=None, TasaIVA=None, IVA=None, IVAProp=None, IVATerc=None, ImptoReten=None, IVANoRet=None, CredEC=None, GrntDep=None, Comisiones=None, MntTotal=None, MontoNF=None, MontoPeriodo=None, SaldoAnterior=None, VlrPagar=None):
        super(TotalesTypeSub, self).__init__(MntNeto, MntExe, MntBase, MntMargenCom, TasaIVA, IVA, IVAProp, IVATerc, ImptoReten, IVANoRet, CredEC, GrntDep, Comisiones, MntTotal, MontoNF, MontoPeriodo, SaldoAnterior, VlrPagar, )
supermod.TotalesType.subclass = TotalesTypeSub
# end class TotalesTypeSub


class ImptoRetenTypeSub(supermod.ImptoRetenType):
    def __init__(self, TipoImp=None, TasaImp=None, MontoImp=None):
        super(ImptoRetenTypeSub, self).__init__(TipoImp, TasaImp, MontoImp, )
supermod.ImptoRetenType.subclass = ImptoRetenTypeSub
# end class ImptoRetenTypeSub


class ComisionesTypeSub(supermod.ComisionesType):
    def __init__(self, ValComNeto=None, ValComExe=None, ValComIVA=None):
        super(ComisionesTypeSub, self).__init__(ValComNeto, ValComExe, ValComIVA, )
supermod.ComisionesType.subclass = ComisionesTypeSub
# end class ComisionesTypeSub


class OtraMonedaTypeSub(supermod.OtraMonedaType):
    def __init__(self, TpoMoneda=None, TpoCambio=None, MntNetoOtrMnda=None, MntExeOtrMnda=None, MntFaeCarneOtrMnda=None, MntMargComOtrMnda=None, IVAOtrMnda=None, ImpRetOtrMnda=None, IVANoRetOtrMnda=None, MntTotOtrMnda=None):
        super(OtraMonedaTypeSub, self).__init__(TpoMoneda, TpoCambio, MntNetoOtrMnda, MntExeOtrMnda, MntFaeCarneOtrMnda, MntMargComOtrMnda, IVAOtrMnda, ImpRetOtrMnda, IVANoRetOtrMnda, MntTotOtrMnda, )
supermod.OtraMonedaType.subclass = OtraMonedaTypeSub
# end class OtraMonedaTypeSub


class ImpRetOtrMndaTypeSub(supermod.ImpRetOtrMndaType):
    def __init__(self, TipoImpOtrMnda=None, TasaImpOtrMnda=None, VlrImpOtrMnda=None):
        super(ImpRetOtrMndaTypeSub, self).__init__(TipoImpOtrMnda, TasaImpOtrMnda, VlrImpOtrMnda, )
supermod.ImpRetOtrMndaType.subclass = ImpRetOtrMndaTypeSub
# end class ImpRetOtrMndaTypeSub


class DetalleTypeSub(supermod.DetalleType):
    def __init__(self, NroLinDet=None, CdgItem=None, IndExe=None, Retenedor=None, NmbItem=None, DscItem=None, QtyRef=None, UnmdRef=None, PrcRef=None, QtyItem=None, Subcantidad=None, FchElabor=None, FchVencim=None, UnmdItem=None, PrcItem=None, OtrMnda=None, DescuentoPct=None, DescuentoMonto=None, SubDscto=None, RecargoPct=None, RecargoMonto=None, SubRecargo=None, CodImpAdic=None, MontoItem=None):
        super(DetalleTypeSub, self).__init__(NroLinDet, CdgItem, IndExe, Retenedor, NmbItem, DscItem, QtyRef, UnmdRef, PrcRef, QtyItem, Subcantidad, FchElabor, FchVencim, UnmdItem, PrcItem, OtrMnda, DescuentoPct, DescuentoMonto, SubDscto, RecargoPct, RecargoMonto, SubRecargo, CodImpAdic, MontoItem, )
supermod.DetalleType.subclass = DetalleTypeSub
# end class DetalleTypeSub


class CdgItemTypeSub(supermod.CdgItemType):
    def __init__(self, TpoCodigo=None, VlrCodigo=None):
        super(CdgItemTypeSub, self).__init__(TpoCodigo, VlrCodigo, )
supermod.CdgItemType.subclass = CdgItemTypeSub
# end class CdgItemTypeSub


class RetenedorTypeSub(supermod.RetenedorType):
    def __init__(self, IndAgente=None, MntBaseFaena=None, MntMargComer=None, PrcConsFinal=None):
        super(RetenedorTypeSub, self).__init__(IndAgente, MntBaseFaena, MntMargComer, PrcConsFinal, )
supermod.RetenedorType.subclass = RetenedorTypeSub
# end class RetenedorTypeSub


class SubcantidadTypeSub(supermod.SubcantidadType):
    def __init__(self, SubQty=None, SubCod=None):
        super(SubcantidadTypeSub, self).__init__(SubQty, SubCod, )
supermod.SubcantidadType.subclass = SubcantidadTypeSub
# end class SubcantidadTypeSub


class OtrMndaTypeSub(supermod.OtrMndaType):
    def __init__(self, PrcOtrMon=None, Moneda=None, FctConv=None, DctoOtrMnda=None, RecargoOtrMnda=None, MontoItemOtrMnda=None):
        super(OtrMndaTypeSub, self).__init__(PrcOtrMon, Moneda, FctConv, DctoOtrMnda, RecargoOtrMnda, MontoItemOtrMnda, )
supermod.OtrMndaType.subclass = OtrMndaTypeSub
# end class OtrMndaTypeSub


class SubDsctoTypeSub(supermod.SubDsctoType):
    def __init__(self, TipoDscto=None, ValorDscto=None):
        super(SubDsctoTypeSub, self).__init__(TipoDscto, ValorDscto, )
supermod.SubDsctoType.subclass = SubDsctoTypeSub
# end class SubDsctoTypeSub


class SubRecargoTypeSub(supermod.SubRecargoType):
    def __init__(self, TipoRecargo=None, ValorRecargo=None):
        super(SubRecargoTypeSub, self).__init__(TipoRecargo, ValorRecargo, )
supermod.SubRecargoType.subclass = SubRecargoTypeSub
# end class SubRecargoTypeSub


class SubTotInfoTypeSub(supermod.SubTotInfoType):
    def __init__(self, NroSTI=None, GlosaSTI=None, OrdenSTI=None, SubTotNetoSTI=None, SubTotIVASTI=None, SubTotAdicSTI=None, SubTotExeSTI=None, ValSubtotSTI=None, LineasDeta=None):
        super(SubTotInfoTypeSub, self).__init__(NroSTI, GlosaSTI, OrdenSTI, SubTotNetoSTI, SubTotIVASTI, SubTotAdicSTI, SubTotExeSTI, ValSubtotSTI, LineasDeta, )
supermod.SubTotInfoType.subclass = SubTotInfoTypeSub
# end class SubTotInfoTypeSub


class DscRcgGlobalTypeSub(supermod.DscRcgGlobalType):
    def __init__(self, NroLinDR=None, TpoMov=None, GlosaDR=None, TpoValor=None, ValorDR=None, ValorDROtrMnda=None, IndExeDR=None):
        super(DscRcgGlobalTypeSub, self).__init__(NroLinDR, TpoMov, GlosaDR, TpoValor, ValorDR, ValorDROtrMnda, IndExeDR, )
supermod.DscRcgGlobalType.subclass = DscRcgGlobalTypeSub
# end class DscRcgGlobalTypeSub


class ReferenciaTypeSub(supermod.ReferenciaType):
    def __init__(self, NroLinRef=None, TpoDocRef=None, IndGlobal=None, FolioRef=None, RUTOtr=None, FchRef=None, CodRef=None, RazonRef=None):
        super(ReferenciaTypeSub, self).__init__(NroLinRef, TpoDocRef, IndGlobal, FolioRef, RUTOtr, FchRef, CodRef, RazonRef, )
supermod.ReferenciaType.subclass = ReferenciaTypeSub
# end class ReferenciaTypeSub


class SignedInfoTypeSub(supermod.SignedInfoType):
    def __init__(self, CanonicalizationMethod=None, SignatureMethod=None, Reference=None):
        super(SignedInfoTypeSub, self).__init__(CanonicalizationMethod, SignatureMethod, Reference, )
supermod.SignedInfoType.subclass = SignedInfoTypeSub
# end class SignedInfoTypeSub


class CanonicalizationMethodTypeSub(supermod.CanonicalizationMethodType):
    def __init__(self, Algorithm='http://www.w3.org/TR/2001/REC-xml-c14n-20010315'):
        super(CanonicalizationMethodTypeSub, self).__init__(Algorithm, )
supermod.CanonicalizationMethodType.subclass = CanonicalizationMethodTypeSub
# end class CanonicalizationMethodTypeSub


class SignatureMethodTypeSub(supermod.SignatureMethodType):
    def __init__(self, Algorithm=None):
        super(SignatureMethodTypeSub, self).__init__(Algorithm, )
supermod.SignatureMethodType.subclass = SignatureMethodTypeSub
# end class SignatureMethodTypeSub


class ReferenceTypeSub(supermod.ReferenceType):
    def __init__(self, URI=None, Transforms=None, DigestMethod=None, DigestValue=None):
        super(ReferenceTypeSub, self).__init__(URI, Transforms, DigestMethod, DigestValue, )
supermod.ReferenceType.subclass = ReferenceTypeSub
# end class ReferenceTypeSub


class TransformsTypeSub(supermod.TransformsType):
    def __init__(self, Transform=None):
        super(TransformsTypeSub, self).__init__(Transform, )
supermod.TransformsType.subclass = TransformsTypeSub
# end class TransformsTypeSub


class TransformTypeSub(supermod.TransformType):
    def __init__(self, Algorithm=None):
        super(TransformTypeSub, self).__init__(Algorithm, )
supermod.TransformType.subclass = TransformTypeSub
# end class TransformTypeSub


class DigestMethodTypeSub(supermod.DigestMethodType):
    def __init__(self, Algorithm='http://www.w3.org/2000/09/xmldsig#sha1'):
        super(DigestMethodTypeSub, self).__init__(Algorithm, )
supermod.DigestMethodType.subclass = DigestMethodTypeSub
# end class DigestMethodTypeSub


class KeyInfoTypeSub(supermod.KeyInfoType):
    def __init__(self, KeyValue=None, X509Data=None):
        super(KeyInfoTypeSub, self).__init__(KeyValue, X509Data, )
supermod.KeyInfoType.subclass = KeyInfoTypeSub
# end class KeyInfoTypeSub


class KeyValueTypeSub(supermod.KeyValueType):
    def __init__(self, RSAKeyValue=None, DSAKeyValue=None):
        super(KeyValueTypeSub, self).__init__(RSAKeyValue, DSAKeyValue, )
supermod.KeyValueType.subclass = KeyValueTypeSub
# end class KeyValueTypeSub


class RSAKeyValueTypeSub(supermod.RSAKeyValueType):
    def __init__(self, Modulus=None, Exponent=None):
        super(RSAKeyValueTypeSub, self).__init__(Modulus, Exponent, )
supermod.RSAKeyValueType.subclass = RSAKeyValueTypeSub
# end class RSAKeyValueTypeSub


class DSAKeyValueTypeSub(supermod.DSAKeyValueType):
    def __init__(self, P=None, Q=None, G=None, Y=None):
        super(DSAKeyValueTypeSub, self).__init__(P, Q, G, Y, )
supermod.DSAKeyValueType.subclass = DSAKeyValueTypeSub
# end class DSAKeyValueTypeSub


class X509DataTypeSub(supermod.X509DataType):
    def __init__(self, X509Certificate=None):
        super(X509DataTypeSub, self).__init__(X509Certificate, )
supermod.X509DataType.subclass = X509DataTypeSub
# end class X509DataTypeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DocumentoCedible'
        rootClass = supermod.DocumentoCedible
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:SiiDte="http://www.sii.cl/SiiDte"',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DocumentoCedible'
        rootClass = supermod.DocumentoCedible
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = None
    doc = parsexml_(StringIO(inString), parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DocumentoCedible'
        rootClass = supermod.DocumentoCedible
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:SiiDte="http://www.sii.cl/SiiDte"')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = None
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'DocumentoCedible'
        rootClass = supermod.DocumentoCedible
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    if not silence:
        sys.stdout.write('#from DocumentCedible import *\n\n')
        sys.stdout.write('import DocumentCedible as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
