#!/bin/bash
# Script per eseguire gli esempi di Sbargold (Linux/Mac)

echo ""
echo "========================================"
echo "   ESEMPI LINGUAGGIO SBARGOLD"
echo "========================================"
echo ""

show_menu() {
    echo "Scegli un esempio da eseguire:"
    echo ""
    echo "1. Hello World"
    echo "2. Calcolatrice"
    echo "3. Loop"
    echo "4. Condizionali"
    echo "5. Array"
    echo "6. Fibonacci"
    echo "7. Fattoriale"
    echo "8. Test Completo"
    echo "9. Esci"
    echo ""
}

while true; do
    show_menu
    read -p "Inserisci la tua scelta (1-9): " choice
    echo ""
    
    case $choice in
        1)
            echo "=== HELLO WORLD ==="
            python3 sbargold.py examples/hello_world.sbg
            echo ""
            read -p "Premi ENTER per continuare..."
            ;;
        2)
            echo "=== CALCOLATRICE ==="
            python3 sbargold.py examples/calculator.sbg
            echo ""
            read -p "Premi ENTER per continuare..."
            ;;
        3)
            echo "=== LOOP ==="
            python3 sbargold.py examples/loop.sbg
            echo ""
            read -p "Premi ENTER per continuare..."
            ;;
        4)
            echo "=== CONDIZIONALI ==="
            python3 sbargold.py examples/conditional.sbg
            echo ""
            read -p "Premi ENTER per continuare..."
            ;;
        5)
            echo "=== ARRAY ==="
            python3 sbargold.py examples/arrays.sbg
            echo ""
            read -p "Premi ENTER per continuare..."
            ;;
        6)
            echo "=== FIBONACCI ==="
            python3 sbargold.py examples/fibonacci.sbg
            echo ""
            read -p "Premi ENTER per continuare..."
            ;;
        7)
            echo "=== FATTORIALE ==="
            python3 sbargold.py examples/factorial.sbg
            echo ""
            read -p "Premi ENTER per continuare..."
            ;;
        8)
            echo "=== TEST COMPLETO ==="
            python3 sbargold.py examples/test_all.sbg
            echo ""
            read -p "Premi ENTER per continuare..."
            ;;
        9)
            echo "Arrivederci!"
            exit 0
            ;;
        *)
            echo "Scelta non valida!"
            read -p "Premi ENTER per continuare..."
            ;;
    esac
    
    clear
    echo ""
    echo "========================================"
    echo "   ESEMPI LINGUAGGIO SBARGOLD"
    echo "========================================"
    echo ""
done
