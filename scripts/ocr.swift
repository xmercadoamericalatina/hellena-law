// OCR de PDF e imagens com o framework Vision do macOS (sem dependências externas).
// Uso: ocr arquivo.pdf ou imagem -> texto em UTF-8 no stdout, páginas separadas por \f
//
// Ordem de leitura: o Vision devolve as linhas soltas, com a caixa de cada uma. Ordenar tudo de
// cima para baixo funciona em página de uma coluna e destrói uma de duas: as linhas das duas
// colunas estão na mesma altura, então saem intercaladas, uma de cada, e o texto vira um
// amálgama ilegível. Era o defeito que o acervo listava como "sem correção automática".
//
// A correção é geométrica, não estatística: procura-se uma calha vertical — uma faixa de x que
// quase nenhuma linha atravessa — e, achando-a, emite-se a coluna da esquerda inteira e depois a
// da direita. Quando não há calha, nada muda em relação ao comportamento antigo.
import AppKit
import Foundation
import PDFKit
import Vision
import ImageIO

// --diagnostico: em vez do texto, relata por página se uma calha foi encontrada e onde. Serve
// para medir quantas páginas do acervo são de duas colunas antes de reprocessar qualquer coisa.
let argumentos = CommandLine.arguments.filter { $0 != "--diagnostico" }
let diagnostico = CommandLine.arguments.contains("--diagnostico")
guard argumentos.count > 1 else {
    FileHandle.standardError.write("uso: ocr [--diagnostico] arquivo.pdf ou imagem\n".data(using: .utf8)!)
    exit(2)
}
let entrada = URL(fileURLWithPath: argumentos[1])
let ehPDF = (try? Data(contentsOf: entrada, options: .mappedIfSafe).starts(with: Data("%PDF".utf8))) ?? false
let doc = ehPDF ? PDFDocument(url: entrada) : nil
let fonteImagem = ehPDF ? nil : CGImageSourceCreateWithURL(entrada as CFURL, nil)
guard doc != nil || fonteImagem != nil else {
    FileHandle.standardError.write("documento não reconhecido\n".data(using: .utf8)!)
    exit(2)
}

/// Procura a calha entre duas colunas e devolve sua posição em x (0 a 1), ou nil se a página for
/// de uma coluna só.
///
/// Uma calha é uma faixa estreita de x que quase nenhuma linha atravessa, tendo de cada lado uma
/// fatia substancial do texto. As três condições juntas evitam falso positivo: uma página de uma
/// coluna com um parágrafo curto no meio não tem lados equilibrados, e uma com tabela de duas
/// colunas estreitas não deixa os dois lados cheios.
func calha(_ caixas: [CGRect]) -> CGFloat? {
    guard caixas.count >= 12 else { return nil }  // página curta demais para afirmar qualquer coisa
    let largura = caixas.reduce(0.0) { $0 + $1.width }
    var melhor: (x: CGFloat, cruzam: Int)? = nil
    // só o miolo da página é candidato: calha em 0,2 ou 0,8 não separa duas colunas de texto
    for passo in 40...60 {
        let x = CGFloat(passo) / 100.0
        let cruzam = caixas.filter { $0.minX < x - 0.01 && $0.maxX > x + 0.01 }.count
        let esquerda = caixas.filter { $0.maxX <= x }
        let direita = caixas.filter { $0.minX >= x }
        // cada lado precisa ter pelo menos um quarto das linhas e um quinto da largura somada
        let ladosCheios = esquerda.count >= caixas.count / 4 && direita.count >= caixas.count / 4
            && esquerda.reduce(0.0) { $0 + $1.width } >= largura / 5
            && direita.reduce(0.0) { $0 + $1.width } >= largura / 5
        guard ladosCheios, cruzam <= max(1, caixas.count / 20) else { continue }
        // Coluna de prosa e coluna de tabela têm a mesma geometria de calha e ordens de leitura
        // opostas: prosa se lê coluna a coluna, tabela se lê linha a linha. O que as separa é a
        // largura das linhas — prosa quebra perto da margem da coluna, célula de tabela não.
        // Exige-se que a maioria das linhas de cada lado ocupe mais de 60% da coluna.
        func prosa(_ lado: [CGRect], _ span: CGFloat) -> Bool {
            guard span > 0, !lado.isEmpty else { return false }
            let cheias = lado.filter { $0.width >= span * 0.6 }.count
            return cheias * 2 > lado.count
        }
        let spanE = (esquerda.map { $0.maxX }.max() ?? 0) - (esquerda.map { $0.minX }.min() ?? 0)
        let spanD = (direita.map { $0.maxX }.max() ?? 0) - (direita.map { $0.minX }.min() ?? 0)
        guard prosa(esquerda, spanE), prosa(direita, spanD) else { continue }
        if melhor == nil || cruzam < melhor!.cruzam { melhor = (x, cruzam) }
    }
    return melhor?.x
}

let escala: CGFloat = 2.5  // ~180 dpi: bom equilíbrio entre precisão e tempo
var saida = ""

let paginas = doc?.pageCount ?? fonteImagem.map { CGImageSourceGetCount($0) } ?? 0
for i in 0..<paginas {
    let imagem: CGImage
    if let fonte = fonteImagem {
        guard let original = CGImageSourceCreateImageAtIndex(fonte, i, nil) else { continue }
        imagem = original
    } else {
    guard let pagina = doc?.page(at: i) else { continue }
    let caixa = pagina.bounds(for: .mediaBox)
    let largura = Int(caixa.width * escala), altura = Int(caixa.height * escala)
    guard let ctx = CGContext(data: nil, width: largura, height: altura, bitsPerComponent: 8, bytesPerRow: 0,
                              space: CGColorSpaceCreateDeviceRGB(),
                              bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue) else { continue }
    ctx.setFillColor(CGColor(red: 1, green: 1, blue: 1, alpha: 1))
    ctx.fill(CGRect(x: 0, y: 0, width: largura, height: altura))
    ctx.scaleBy(x: escala, y: escala)
    pagina.draw(with: .mediaBox, to: ctx)
    guard let renderizada = ctx.makeImage() else { continue }
    imagem = renderizada
    }

    let pedido = VNRecognizeTextRequest()
    pedido.recognitionLevel = .accurate
    pedido.recognitionLanguages = ["pt-BR"]
    pedido.usesLanguageCorrection = true
    do {
        try VNImageRequestHandler(cgImage: imagem, options: [:]).perform([pedido])
    } catch {
        FileHandle.standardError.write("OCR página \(i + 1): \(error)\n".data(using: .utf8)!)
        continue
    }

    let observacoes = pedido.results ?? []
    // o Vision usa origem no canto inferior esquerdo: maior maxY é mais alto na página
    func deCimaParaBaixo(_ obs: [VNRecognizedTextObservation]) -> [String] {
        obs.sorted { $0.boundingBox.maxY > $1.boundingBox.maxY }
           .compactMap { $0.topCandidates(1).first?.string }
    }

    if diagnostico {
        let x = calha(observacoes.map { $0.boundingBox })
        saida += "pagina \(i + 1): linhas=\(observacoes.count) calha=" +
                 (x.map { String(format: "%.2f", $0) } ?? "nenhuma") + "\n"
        continue
    }

    var linhas: [String]
    if let x = calha(observacoes.map { $0.boundingBox }) {
        // o que atravessa a calha é cabeçalho, rodapé ou título de página inteira: vai na frente
        let cruzam = observacoes.filter { $0.boundingBox.minX < x - 0.01 && $0.boundingBox.maxX > x + 0.01 }
        let esquerda = observacoes.filter { $0.boundingBox.maxX <= x }
        let direita = observacoes.filter { $0.boundingBox.minX >= x }
        linhas = deCimaParaBaixo(cruzam) + deCimaParaBaixo(esquerda) + deCimaParaBaixo(direita)
    } else {
        linhas = deCimaParaBaixo(observacoes)
    }
    saida += linhas.joined(separator: "\n") + "\n\u{0C}"
}

FileHandle.standardOutput.write(saida.data(using: .utf8)!)
