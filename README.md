# recauda-propi
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de Recaudación</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            position: relative; /* Necesario para el botón flotante y el balance */
            padding-bottom: 70px; /* Espacio para el botón flotante */
            display: flex; /* Para centrar el modal de login */
            justify-content: center; /* Para centrar el modal de login */
            align-items: center; /* Para centrar el modal de login */
            min-height: 100vh; /* Para que el body ocupe toda la altura de la vista */
        }

        /* Estilos para el modal de inicio de sesión */
        #loginOverlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000; /* Asegura que esté por encima de todo */
        }

        #loginBox {
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
            width: 90%;
            max-width: 350px;
            text-align: center;
        }

        #loginBox h2 {
            margin-bottom: 25px;
            color: #333;
        }

        #loginBox label {
            display: block;
            margin-bottom: 10px;
            text-align: left;
            font-weight: bold;
            color: #555;
        }

        #loginBox input[type="text"],
        #loginBox input[type="password"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 16px;
        }

        #loginBox button {
            width: 100%;
            padding: 12px;
            background-color: #007bff;
            border: none;
            border-radius: 4px;
            color: white;
            font-size: 18px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        #loginBox button:hover {
            background-color: #0056b3;
        }

        #loginMessage {
            color: red;
            margin-top: 15px;
            font-weight: bold;
        }

        /* Oculta el contenido principal por defecto */
        #mainContent {
            display: none;
            width: 100%;
        }

        h2, h3 {
            text-align: center;
            color: #333;
        }

        /* Ajuste para el título h2 para dejar espacio al punto actual */
        h2 {
            margin-top: 50px; /* Aumenta el margen superior para que no se solape con el punto actual */
        }

        .form-container, .table-container {
            background-color: #fff;
            padding: 20px;
            margin: 20px auto;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 400px;
        }

        /* Contenedor del punto actual en la esquina superior derecha */
        .top-right-balance {
            position: absolute; 
            top: 25px; /* Mantener la distancia del top */
            right: 25px; /* Mantener la distancia de la derecha */
            background-color: #f0f0f0;
            padding: 8px 12px;
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            display: flex; 
            align-items: center; 
            font-size: 14px;
            color: #333;
            z-index: 999; 
            white-space: nowrap; 
        }

        .top-right-balance .edit-balance-btn {
            background: none;
            border: none;
            color: #007bff; 
            cursor: pointer;
            font-size: 14px;
            margin-left: 8px; 
            padding: 0; 
            transition: color 0.2s ease;
        }
        .top-right-balance .edit-balance-btn:hover {
            color: #0056b3;
        }
        .top-right-balance .edit-balance-btn i {
            pointer-events: none; 
        }


        .controls-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 20px auto;
            max-width: 900px; 
            padding: 0 20px;
        }

        /* Contenedor específico para los botones principales para que se ordenen mejor */
        .main-buttons-group {
            display: flex;
            flex-wrap: wrap; 
            gap: 8px; 
            justify-content: center;
            width: 100%; 
            margin-bottom: 10px; 
        }

        /* Oculta los grupos de control de filtro por defecto */
        .control-group, #btnReiniciarFiltros {
            display: none; 
        }

        /* Cuando la tabla no está minimizada, muestra los filtros */
        .controls-expanded .control-group,
        .controls-expanded #btnReiniciarFiltros {
            display: block; 
        }


        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
            color: #555;
        }

        input[type="date"],
        input[type="tel"],
        select {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }

        button {
            padding: 8px 12px; 
            background-color: #28a745;
            border: none;
            border-radius: 4px;
            color: white;
            font-size: 14px; 
            cursor: pointer;
            transition: background-color 0.3s ease;
            white-space: nowrap; 
        }

        button:hover {
            background-color: #218838;
        }

        .button-delete {
            background-color: #dc3545;
        }

        .button-delete:hover {
                background-color: #c82333;
        }

        .button-reset {
            background-color: #007bff;
        }

        .button-reset:hover {
            background-color: #0056b3;
        }

        .button-copy {
            background-color: #ffc107; 
            color: #333;
        }
        .button-copy:hover {
            background-color: #e0a800; 
        }
        
        /* Estilos para el botón de ir a datos (arriba, con ícono) */
        .button-to-data {
            background-color: #6c757d;
            color: white;
            padding: 8px 12px; 
            display: flex; 
            align-items: center;
            justify-content: center;
            font-size: 14px; 
        }
        .button-to-data:hover {
            background-color: #5a6268;
        }
        .button-to-data i {
            font-size: 16px; 
            margin-right: 5px; 
        }
        /* Si no hay texto, ajusta el padding */
        .button-to-data:not(:has(span)) i {
            margin-right: 0;
        }


        /* Estilos para el botón flotante de ir al inicio */
        .fab-scroll-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: #030406c5;
            color: white;
            border-radius: 50%; 
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            z-index: 1000; 
            transition: background-color 0.3s ease, transform 0.3s ease, opacity 0.3s ease, visibility 0.3s ease; 
            opacity: 0; 
            visibility: hidden; 
        }
        .fab-scroll-to-top.show {
            opacity: 1; 
            visibility: visible; 
        }
        .fab-scroll-to-top:hover {
            background-color: #0056b3;
            transform: scale(1.05); 
        }
        .fab-scroll-to-top i {
            margin: 0; 
        }


        .table-container {
            overflow-x: auto;
            background-color: #fff;
            padding: 20px;
            margin: 20px auto;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            max-width: 900px; 
            scroll-margin-top: 20px; 
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }

        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }

        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }

        tfoot td {
            font-weight: bold;
            background-color: #f9f9f9;
            text-align: left;
        }

        tfoot tr {
            background-color: #f2f2f2;
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1001; /* Z-index alto para que esté por encima de todo */
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.4);
            padding-top: 60px;
        }

        .modal-content {
            background-color: #fefefe;
            margin: 5% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 80%;
            max-width: 500px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .modal-content textarea {
            width: calc(100% - 20px); 
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
            resize: vertical; 
        }

        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }

        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }

        /* Estilos para pantallas pequeñas */
        @media (max-width: 600px) {
            .top-right-balance {
                position: relative; /* Vuelve a ser relativo para que ocupe espacio en el flujo */
                width: 90%; 
                margin: 10px auto; /* Centra y da margen */
                top: auto; /* Resetea el top absoluto */
                right: auto; /* Resetea el right absoluto */
                justify-content: center; 
            }

            /* Asegurarse de que el h2 siempre esté debajo del punto actual en móviles */
            h2 {
                margin-top: 20px; /* Un margen superior suficiente en móviles */
            }

            .controls-container {
                flex-direction: column;
                align-items: center;
            }

            .main-buttons-group {
                flex-direction: row; 
                justify-content: center;
                width: 100%;
            }
            .main-buttons-group button {
                flex-grow: 1; 
                min-width: unset; 
                font-size: 13px; 
                padding: 7px 10px; 
            }
            /* Si son muchos, que bajen y ocupen la mitad cada uno */
            .main-buttons-group button:nth-child(odd):last-child { 
                width: 100%;
            }
            .main-buttons-group button:nth-child(even),
            .main-buttons-group button:nth-child(odd):not(:last-child) { 
                 width: calc(50% - 4px); 
            }


            .control-group {
                min-width: unset;
                width: 100%;
            }

            table, thead, tbody, th, td, tr {
                display: block;
            }

            thead tr {
                position: absolute;
                top: -9999px;
                left: -9999px;
            }

            tr {
                border: 1px solid #ccc;
                margin-bottom: 10px;
                display: flex;
                flex-wrap: wrap;
            }

            td {
                border: none;
                border-bottom: 1px solid #eee;
                position: relative;
                padding-left: 50%;
                text-align: right;
                width: 100%;
            }

            td:before {
                content: attr(data-label);
                position: absolute;
                left: 6px;
                width: 45%;
                padding-right: 10px;
                white-space: nowrap;
                text-align: left;
                font-weight: bold;
            }
            tfoot tr {
                display: flex;
                flex-wrap: wrap;
                width: 100%;
                border: 1px solid #ccc;
                margin-top: 10px;
            }
            tfoot td {
                width: 100%;
                text-align: right;
                padding-left: 50%;
            }
            tfoot td:first-child {
                text-align: left;
            }
            tfoot td[colspan="2"] {
                width: calc(100% - 12px); 
            }
        }
    </style>
</head>
<body>
    <div id="loginOverlay">
        <div id="loginBox">
            <h2>Acceso Requerido</h2>
            <form id="loginForm">
                <label for="username">Usuario:</label>
                <input type="text" id="username" required autocomplete="username">
                <label for="password">Contraseña:</label>
                <input type="password" id="password" required autocomplete="current-password">
                <button type="submit">Entrar</button>
                <p id="loginMessage" style="display: none;"></p>
            </form>
        </div>
    </div>

    <div id="mainContent">
        <div class="top-right-balance" id="topRightBalance">
            Punto Actual: <span id="displaySaldoGuardado"></span> 
            (<span id="displayFechaSaldo"></span>)
            <button class="edit-balance-btn" id="btnEditBalance" title="Editar Punto Actual">
                <i class="fas fa-pencil-alt"></i>
            </button>
        </div>

        <h2>Datos Recaudados</h2>
        <h3>Total Recaudado: <span id="totalRecaudado"></span></h3>

        <div class="controls-container" id="controlsContainer">
            <div class="main-buttons-group">
                <button id="btnAgregarDato">Agregar Dato</button>
                <button id="btnMinimizarTabla">Maximizar Tabla</button> 
                <button id="btnImportarDatos" class="button-copy">Importar Datos</button>
                <button id="btnOrdenarFechaAsc" class="button-reset">Fecha (Antiguo)</button>
                <button id="btnOrdenarFechaDesc" class="button-reset">Fecha (Reciente)</button>
                <button id="scrollToDataBtn" class="button-to-data" title="Ir a los datos">
                    <i class="fas fa-chart-bar"></i> <span>Ir al Historial</span>
                </button>
            </div>
            
            <div class="control-group">
                <label for="filtroFechas">Filtrar por fechas específicas (AAAA-MM-DD):</label>
                <input type="text" id="filtroFechas" placeholder="Ej: 2023-01-01, 2023-01-05">
            </div>
            <div class="control-group">
                <label for="filtroFechaInicio">Filtrar desde:</label>
                <input type="date" id="filtroFechaInicio">
            </div>
            <div class="control-group">
                <label for="filtroFechaFin">hasta:</label>
                <input type="date" id="filtroFechaFin">
            </div>
            <button id="btnReiniciarFiltros" class="button-reset">Reiniciar Filtros</button>
        </div>

        <div class="table-container" id="tableContainerScrollTarget">
            <div id="tablaContainer"></div>
        </div>

        <div id="scrollToTopBtn" class="fab-scroll-to-top" title="Ir al inicio">
            <i class="fas fa-arrow-up">↑</i>
        </div>

        <div id="agregarModal" class="modal">
            <div class="modal-content">
                <span class="close" data-modal-id="agregarModal">×</span>
                <h2>Agregar Datos</h2>
                <form id="agregarForm">
                    <label for="tipo">Tipo:</label>
                    <select id="tipo" name="tipo">
                        <option value="Máquinas">Máquinas</option>
                        <option value="Mesas">Mesas</option>
                        <option value="Otras">Otras</option>
                    </select><br><br>
                    <label for="fecha">Fecha:</label>
                    <input type="date" id="fecha" name="fecha" required><br><br>
                    <label for="monto">Monto Recaudado:</label>
                    <input type="tel" id="monto" name="monto" oninput="formatearMonto(this)" required><br><br>
                    <button type="submit">Agregar</button>
                </form>
            </div>
        </div>

        <div id="editModal" class="modal">
            <div class="modal-content">
                <span class="close" data-modal-id="editModal">×</span>
                <h2>Editar Datos</h2>
                <form id="editarForm">
                    <label for="editarTipo">Tipo:</label>
                    <select id="editarTipo" name="editarTipo">
                        <option value="Máquinas">Máquinas</option>
                        <option value="Mesas">Mesas</option>
                        <option value="Otras">Otras</option>
                    </select><br><br>
                    <label for="editarFecha">Fecha:</label>
                    <input type="date" id="editarFecha" name="editarFecha" required><br><br>
                    <label for="editarMonto">Monto Recaudado:</label>
                    <input type="tel" id="editarMonto" name="editarMonto" oninput="formatearMonto(this)" required><br><br>
                    <button type="submit">Guardar</button>
                </form>
            </div>
        </div>

        <div id="editBalanceModal" class="modal">
            <div class="modal-content">
                <span class="close" data-modal-id="editBalanceModal">×</span>
                <h2>Editar Punto Actual</h2>
                <form id="editBalanceForm">
                    <div style="margin-bottom: 15px;"> 
                        <label for="editBalanceDate">Fecha del Punto:</label>
                        <input type="date" id="editBalanceDate" name="editBalanceDate" required>
                    </div>
                    <label for="editSaldoActual">Monto del Punto:</label>
                    <input type="tel" id="editSaldoActual" name="editSaldoActual" oninput="formatearMonto(this)" required><br><br>
                    <button type="submit">Guardar Punto</button>
                </form>
            </div>
        </div>

        <div id="importarModal" class="modal">
            <div class="modal-content">
                <span class="close" data-modal-id="importarModal">×</span>
                <h2>Importar Datos desde Texto</h2>
                <p>Pega aquí el texto de los datos de recaudación (ej. desde WhatsApp):</p>
                <textarea id="importDataTextarea" rows="10" cols="50" placeholder="Pega el texto aquí..."></textarea><br><br>
                <button id="btnProcesarImportacion">Procesar Importación</button>
            </div>
        </div>
    </div>

    <script>
        // --- Bloqueo por Contraseña ---
        const VALID_USERNAME = 'croupier'; // Puedes c