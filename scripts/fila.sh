#!/bin/sh
# Encadeia as coletas longas, uma fila por servidor de origem.
#
# A razão de existir é o limite de taxa: cada fonte aceita de 1 a 4 requisições por segundo, e esse
# limite é por servidor, não por processo. Rodar dois baixadores contra o normas.leg.br ao mesmo
# tempo dobraria a taxa real. Então cada fila é sequencial, e as filas de servidores diferentes
# correm em paralelo.
#
# Todos os baixadores são retomáveis: pulam o que já existe. Interromper e rodar de novo é seguro,
# e é assim que se retoma depois de desligar a máquina.
#
#   sh scripts/fila.sh senado    # normas.leg.br: resoluções, decretos legislativos, decretos
#   sh scripts/fila.sh dou 2025 2002   # in.gov.br: um ano por vez, do mais recente para trás
#
# A saída de cada etapa vai para _log_<fila>.txt na raiz do repositório.

set -e
cd "$(dirname "$0")/.."
FILA="$1"

case "$FILA" in
senado)
  # Espera a coleta do Congresso em curso terminar, para não dobrar a taxa no mesmo servidor.
  while pgrep -f "baixar_federal.py --tipos DLG" > /dev/null; do sleep 60; done

  # Da série menor para a maior: as resoluções fecham em minutos, os decretos levam um dia.
  python3 -I scripts/baixar_federal.py --tipos RSF,RCN,RRC --workers 4 --rps 4
  python3 -I scripts/baixar_federal.py --tipos DEC-sn      --workers 4 --rps 4
  python3 -I scripts/baixar_federal.py --tipos DEC-n       --workers 4 --rps 4
  ;;

dou)
  # Do ano mais recente para trás: o infralegal recente é o que mais se consulta. O texto online
  # do DOU começa em 2002; antes disso a Imprensa Nacional só tem a imagem digitalizada.
  while pgrep -f "baixar_dou.py" > /dev/null; do sleep 60; done
  DE="${2:-2025}"
  ATE="${3:-2002}"
  ANO="$DE"
  FALHOU=0
  while [ "$ANO" -ge "$ATE" ]; do
    if python3 -I scripts/baixar_dou.py --de "$ANO-01-01" --ate "$ANO-12-31" --workers 4 --rps 3; then
      :
    else
      CODIGO=$?
      if [ "$CODIGO" -eq 77 ]; then
        echo "fila DOU interrompida: fonte recusou acesso; não iniciar outro ano" >&2
        exit 77
      fi
      FALHOU=1
      echo "DOU $ANO incompleto; consultar reguladores/_falhas.jsonl e retomar o ano" >&2
    fi
    ANO=$((ANO - 1))
  done
  if [ "$FALHOU" -ne 0 ]; then
    echo "fila DOU terminou com pendências" >&2
    exit 1
  fi
  ;;

*)
  echo "uso: sh scripts/fila.sh senado | dou [ano_inicial] [ano_final]" >&2
  exit 2
  ;;
esac

echo "fila $FILA concluída"
