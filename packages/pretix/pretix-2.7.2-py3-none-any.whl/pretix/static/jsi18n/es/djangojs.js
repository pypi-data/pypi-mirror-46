

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=n != 1;
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "(one more date)": [
      "(una fecha m\u00e1s)",
      "({num} fechas m\u00e1s)"
    ],
    "All": "Todos",
    "An error has occurred.": "Ha ocurrido un error.",
    "An error of type {code} occurred.": "Ha ocurrido un error de tipo {code}.",
    "April": "Abril",
    "August": "Agosto",
    "Barcode area": "\u00c1rea para c\u00f3digo de barras",
    "Cart expired": "El carrito de compras ha expirado",
    "Check-in QR": "QR de Chequeo",
    "Click to close": "Click para cerrar",
    "Close message": "Cerrar mensaje",
    "Comment:": "Comentario:",
    "Contacting Stripe \u2026": "Contactando con Stripe\u2026",
    "Copied!": "\u00a1Copiado!",
    "Count": "Cantidad",
    "December": "Diciembre",
    "Do you really want to leave the editor without saving your changes?": "\u00bfRealmente desea salir del editor sin haber guardado sus cambios?",
    "Error while uploading your PDF file, please try again.": "Ha habido un error mientras se cargaba el archivo PDF, por favor, intente de nuevo.",
    "February": "Febrero",
    "Fr": "Vi",
    "Generating messages \u2026": "Generando mensajes\u2026",
    "Group of objects": "Grupo de objetos",
    "January": "Enero",
    "July": "Julio",
    "June": "Junio",
    "Lead Scan QR": "Escanear QR de clientes potenciales",
    "March": "Marzo",
    "Marked as paid": "Marcado como pagado",
    "May": "Mayo",
    "Mo": "Me",
    "No": "No",
    "None": "Ninguno",
    "November": "Noviembre",
    "Object": "Objeto",
    "October": "Octubre",
    "Others": "Otros",
    "Paid orders": "\u00d3rdenes pagadas",
    "Placed orders": "\u00d3rdenes enviadas",
    "Powered by pretix": "Prove\u00eddo por pretix",
    "Press Ctrl-C to copy!": "\u00a1Presione Control+C para copiar!",
    "Sa": "S\u00e1",
    "Saving failed.": "El guardado fall\u00f3.",
    "September": "Septiembre",
    "Su": "Do",
    "Text object": "Objeto de texto",
    "Th": "Ju",
    "The PDF background file could not be loaded for the following reason:": "El fondo del archivo PDF no ha podido ser cargado por la siguiente raz\u00f3n:",
    "The items in your cart are no longer reserved for you.": "Los elementos en su carrito de compras han dejado de estar reservados.",
    "The items in your cart are reserved for you for one minute.": [
      "Los elementos en su carrito de compras se han reservado por un minuto.",
      "Los elementos en su carrito de compras se han reservado por {num} minutos."
    ],
    "The request took to long. Please try again.": "La solicitud ha tomado demasiado tiempo. Por favor, pruebe de nuevo.",
    "Ticket design": "Dise\u00f1o del ticket",
    "Total": "Total",
    "Total revenue": "Ingresos totales",
    "Tu": "Ma",
    "Unknown error.": "Error desconocido.",
    "Use a different name internally": "Usar un nombre diferente internamente",
    "We": "Mie",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "Estamos enviando su solicitud al servidor. Si este proceso toma m\u00e1s de un minuto, por favor, revise su conexi\u00f3n a Internet, recargue la p\u00e1gina y pruebe de nuevo.",
    "We are processing your request \u2026": "Estamos procesando su solicitud\u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "Ahora mismo no podemos contactar con el servidor, pero lo seguimos intentando. El \u00faltimo c\u00f3digo de error fue: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "Ahora mismo no podemos contactar con el servidor. Por favor, pruebe de nuevo. C\u00f3digo de error: {code}",
    "Yes": "Si",
    "Your color has bad contrast for text on white background, please choose a darker shade.": "Tu color tiene mal contraste para un texto con fondo blanco, por favor escoge un tono m\u00e1s oscuro.",
    "Your color has decent contrast and is probably good-enough to read!": "\u00a1Tu color tiene un contraste decente y es probablemente suficientemente legible!",
    "Your color has great contrast and is very easy to read!": "\u00a1Tu color tiene gran contraste y es muy legible!",
    "Your request arrived on the server but we still wait for it to be processed. If this takes longer than two minutes, please contact us or go back in your browser and try again.": "Su solicitud lleg\u00f3 al servidor pero seguimos esperando a que sea procesada. Si toma m\u00e1s de dos minutos, por favor cont\u00e1ctenos o regrese a la p\u00e1gina anterior en su navegador y pruebe de nuevo.",
    "Your request has been queued on the server and will now be processed. Depending on the size of your event, this might take up to a few minutes.": "Su solicitud ha sido enviada al servidor y ser\u00e1 procesada en breve. Esto puede tomar uno o varios minutos, en dependencia del tama\u00f1o de su evento.",
    "widget\u0004<a href=\"https://pretix.eu\" target=\"_blank\" rel=\"noopener\">event ticketing powered by pretix</a>": "<a href=\"https://pretix.eu\" target=\"_blank\" rel=\"noopener\">tickets para eventos cortes\u00eda de pretix</a>",
    "widget\u0004Back": "Atr\u00e1s",
    "widget\u0004Buy": "Comprar",
    "widget\u0004Choose a different event": "Elige un evento diferente",
    "widget\u0004Close": "Cerrar",
    "widget\u0004Close ticket shop": "Cerrar tienda de tickets",
    "widget\u0004Continue": "Continuar",
    "widget\u0004FREE": "GRATIS",
    "widget\u0004Next month": "Siguiente mes",
    "widget\u0004Only available with a voucher": "Solo disponible mediante voucher",
    "widget\u0004Previous month": "Mes anterior",
    "widget\u0004Redeem": "Utilizar cup\u00f3n",
    "widget\u0004Redeem a voucher": "Utilizar un cup\u00f3n",
    "widget\u0004Reserved": "Reservado",
    "widget\u0004Resume checkout": "Reanudar pago",
    "widget\u0004See variations": "Ver variaciones",
    "widget\u0004Sold out": "Agotado",
    "widget\u0004The cart could not be created. Please try again later": "El carrito de compras no ha podido crearse. Por favor, pruebe de nuevo m\u00e1s tarde",
    "widget\u0004The ticket shop could not be loaded.": "No se ha podido cargar la tienda de tickets.",
    "widget\u0004Voucher code": "C\u00f3digo del cup\u00f3n",
    "widget\u0004Waiting list": "Lista de espera",
    "widget\u0004You currently have an active cart for this event. If you select more products, they will be added to your existing cart.": "Ya tiene un carrito de compras activo para este evento. Si selecciona m\u00e1s productos, estos ser\u00e1n a\u00f1adidos al carrito actual.",
    "widget\u0004currently available: %s": "disponible actualmente: %s",
    "widget\u0004from %(currency)s %(price)s": "a partir de %(currency)s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "incluye %(rate)s% %(taxname)s",
    "widget\u0004incl. taxes": "incl. impuestos",
    "widget\u0004minimum amount to order: %s": "cantidad m\u00ednima a ordenar: %s",
    "widget\u0004plus %(rate)s% %(taxname)s": "m\u00e1s %(rate)s% %(taxname)s",
    "widget\u0004plus taxes": "m\u00e1s impuestos"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j \\d\\e F \\d\\e Y \\a \\l\\a\\s H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%y %H:%M:%S",
      "%d/%m/%y %H:%M:%S.%f",
      "%d/%m/%y %H:%M",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j \\d\\e F \\d\\e Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j \\d\\e F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i",
    "SHORT_DATE_FORMAT": "d/m/Y",
    "THOUSAND_SEPARATOR": ".",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

