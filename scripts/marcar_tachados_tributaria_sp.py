"""Restaura distinções visuais de dois trechos do PDF oficial, sem decidir efeitos."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
DOC = Path('municipais/SP/sao-paulo/decretos/2026/decreto-65599-2026.md')
OLD = '7808f6169dd90ce01a23586a40af5e90b426d6d808459e5e0c9754b3060c89fb'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    dest = ROOT / 'municipais/_lotes/20261020-sp-tributaria-tachados'
    dest.mkdir(exist_ok=False)
    path = ROOT / DOC
    raw = path.read_bytes()
    if sha(raw) != OLD:
        raise ValueError('Documento diverge do snapshot revisado; não aplicar')
    (dest / 'documento-anterior.md').write_bytes(raw)
    text = raw.decode()
    pairs = [
        (70, 'I - à expedição de "Habite-se" ou "Auto de Vistoria" e à conservação de obras particulares;'),
        (203, 'Quando o PAT incluir débitos de Imposto Sobre Serviços de Qualquer Natureza – ISS\nrelativos a obra, o certificado de quitação do ISS, para fins de emissão de certificado de conclusão\nou auto de vistoria ou de conservação de obras particulares, bem como no caso de pagamento de\nobras contratadas com o Município de São Paulo, somente será expedido com o pagamento\nintegral do referido acordo de parcelamento. (Art. 13 da Lei nº 14.256, de 29/12/06)')]
    for page, trecho in pairs:
        if text.count(trecho) != 1:
            raise ValueError('Trecho não é único')
        label = f'[INÍCIO DO TRECHO TACHADO NA FONTE OFICIAL, página {page}]'
        replacement = label + '\n' + trecho + '\n[FIM DO TRECHO TACHADO NA FONTE OFICIAL]'
        text = text.replace(trecho, replacement)
    note = ('Nota de transcrição: o PDF oficial apresenta tachados no inciso I do art. 260 (página 70) '
            'e no corpo do art. 869 (página 203). Os trechos foram preservados entre rótulos explícitos, '
            'junto às notas literais da fonte sobre revogação com efeitos a partir do ato de SF. '
            'A marcação reproduz a edição da fonte e não determina o cumprimento dessa condição.\n\n')
    text = text.replace('```text\n', note + '```text\n', 1)
    text = text.replace('anexo preformatado e três tabelas em imagem transcritas e conferidas visualmente"',
                        'anexo preformatado e três tabelas em imagem transcritas e conferidas visualmente; dois trechos tachados identificados conforme PDF, com notas condicionais preservadas"')
    old_body = raw.decode().split('\n\n# ', 1)[1].split('\n\n', 1)[1].rstrip('\n')
    body = text.split('\n\n# ', 1)[1].split('\n\n', 1)[1].rstrip('\n')
    text = re.sub(r'(?m)^sha256_texto: "[a-f0-9]+"$', 'sha256_texto: "' + sha(body.encode()) + '"', text)
    # Restituir os rótulos e a nota deve recuperar integralmente o corpo anterior.
    restored = body.replace(note, '')
    for page, trecho in pairs:
        restored = restored.replace(f'[INÍCIO DO TRECHO TACHADO NA FONTE OFICIAL, página {page}]\n' + trecho + '\n[FIM DO TRECHO TACHADO NA FONTE OFICIAL]', trecho)
    if restored != old_body:
        raise ValueError('Mudança textual fora dos dois rótulos e da nota')
    path.write_text(text)
    evidence = [Path('municipais/_referencias/auditorias/tachados-capitais-20261020') / ('sp-tributaria-' + str(page) + '.png') for page, _ in pairs]
    records = [{'arquivo': str(p), 'sha256': sha((ROOT / p).read_bytes()), 'bytes': (ROOT / p).stat().st_size} for p in evidence + [Path(__file__).relative_to(ROOT)]]
    receipt = {'documento': str(DOC), 'sha256_anterior': OLD, 'sha256_novo': sha(path.read_bytes()),
               'backup': str((dest / 'documento-anterior.md').relative_to(ROOT)),
               'sha256_corpo_novo': sha(body.encode()), 'paginas': [70, 203], 'provas': records,
               'verificacao': 'Corpo anterior recuperado exatamente ao retirar somente os rótulos e a nota. Três tabelas e notas condicionais literais inalteradas.',
               'limite': 'Marca visual confirmada, sem inferir o cumprimento da condição do ato de SF.'}
    (dest / 'manifesto.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == '__main__':
    main()
