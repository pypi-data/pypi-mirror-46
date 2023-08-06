

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=n > 1;
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
      "(une date en plus)",
      "({num} plus de dates)"
    ],
    "All": "Tous",
    "An error has occurred.": "Une erreur s'est produite.",
    "An error of type {code} occurred.": "Une erreur de type {code} s'est produite.",
    "Barcode area": "Zone de code-barres",
    "Cart expired": "Panier expir\u00e9",
    "Check-in QR": "Enregistrement QR code",
    "Close message": "Fermer le message",
    "Comment:": "Commentaire :",
    "Contacting Stripe \u2026": "Contacter Stripe \u2026",
    "Copied!": "Copi\u00e9 !",
    "Count": "Compter",
    "Do you really want to leave the editor without saving your changes?": "Voulez-vous vraiment quitter l'\u00e9diteur sans sauvegarder vos modifications ?",
    "Error while uploading your PDF file, please try again.": "Erreur lors du t\u00e9l\u00e9chargement de votre fichier PDF, veuillez r\u00e9essayer.",
    "Generating messages \u2026": "Cr\u00e9ation de messages \u2026",
    "Group of objects": "Groupe d'objets",
    "Lead Scan QR": "Balayage du QR code",
    "Marked as paid": "Marqu\u00e9 comme pay\u00e9",
    "None": "Aucun",
    "Object": "Objet",
    "Others": "Autres",
    "Paid orders": "Ordres pay\u00e9s",
    "Placed orders": "Commandes pass\u00e9es",
    "Powered by pretix": "G\u00e9n\u00e9r\u00e9 par pretix",
    "Press Ctrl-C to copy!": "Appuyez sur Ctrl-C pour copier !",
    "Saving failed.": "L'enregistrement a \u00e9chou\u00e9.",
    "Text object": "Objet texte",
    "The PDF background file could not be loaded for the following reason:": "Le fichier PDF g\u00e9n\u00e9r\u00e9 en arri\u00e8re-plan n'a pas pu \u00eatre charg\u00e9 pour la raison suivante :",
    "The items in your cart are no longer reserved for you.": "Les articles de votre panier ne vous sont plus r\u00e9serv\u00e9s.",
    "The items in your cart are reserved for you for one minute.": [
      "Les articles de votre panier vous sont r\u00e9serv\u00e9s pour une minute.",
      "Les articles de votre panier vous sont r\u00e9serv\u00e9s pour {num} minutes."
    ],
    "The request took to long. Please try again.": "La requ\u00eate a prit trop de temps. Veuillez r\u00e9essayer.",
    "Ticket design": "Conception des billets",
    "Total": "Total",
    "Total revenue": "Revenu total",
    "Unknown error.": "Erreur inconnue.",
    "Use a different name internally": "Utiliser un nom diff\u00e9rent en interne",
    "We are currently sending your request to the server. If this takes longer than one minute, please check your internet connection and then reload this page and try again.": "Nous envoyons actuellement votre demande au serveur. Si cela prend plus d'une minute, veuillez v\u00e9rifier votre connexion Internet, puis recharger cette page et r\u00e9essayer.",
    "We are processing your request \u2026": "Nous traitons votre demande \u2026",
    "We currently cannot reach the server, but we keep trying. Last error code: {code}": "Nous ne pouvons actuellement pas atteindre le serveur, mais nous continuons d'essayer. Dernier code d'erreur: {code}",
    "We currently cannot reach the server. Please try again. Error code: {code}": "Actuellement, nous ne pouvons pas atteindre le serveur. Veuillez r\u00e9essayer. Code d'erreur: {code}",
    "Your request has been queued on the server and will now be processed. Depending on the size of your event, this might take up to a few minutes.": "Votre demande a \u00e9t\u00e9 mise en attente sur le serveur et sera trait\u00e9e. Selon la taille de votre \u00e9v\u00e9nement, cela peut prendre jusqu' \u00e0 quelques minutes.",
    "widget\u0004<a href=\"https://pretix.eu\" target=\"_blank\" rel=\"noopener\">event ticketing powered by pretix</a>": "<a href=\"https://pretix.eu\" target=\"_blank\" rel=\"noopener\">Billetterie en ligne propuls\u00e9e par Pretix</a>",
    "widget\u0004Buy": "Acheter",
    "widget\u0004Close": "Fermer",
    "widget\u0004Close ticket shop": "Fermer la billetterie",
    "widget\u0004Continue": "Continuer",
    "widget\u0004FREE": "GRATUIT",
    "widget\u0004Only available with a voucher": "Disponible avec un bon de r\u00e9duction",
    "widget\u0004Redeem": "Echanger",
    "widget\u0004Redeem a voucher": "Utiliser un bon d'achat",
    "widget\u0004Reserved": "R\u00e9serv\u00e9",
    "widget\u0004Resume checkout": "Reprendre le paiement",
    "widget\u0004See variations": "Voir les variations",
    "widget\u0004Sold out": "Epuis\u00e9",
    "widget\u0004The cart could not be created. Please try again later": "Le panier n' a pas pu \u00eatre cr\u00e9\u00e9. Veuillez r\u00e9essayer plus tard",
    "widget\u0004The ticket shop could not be loaded.": "La billetterie n' a pas pu \u00eatre charg\u00e9e.",
    "widget\u0004Voucher code": "Code de r\u00e9duction",
    "widget\u0004Waiting list": "Liste d'attente",
    "widget\u0004You currently have an active cart for this event. If you select more products, they will be added to your existing cart.": "Vous avez actuellement un panier actif pour cet \u00e9v\u00e9nement. Si vous s\u00e9lectionnez d'autres produits, ils seront ajout\u00e9s \u00e0 votre panier.",
    "widget\u0004currently available: %s": "actuellement disponible: %s",
    "widget\u0004from %(currency)s %(price)s": "de %(currency)s %(price)s",
    "widget\u0004incl. %(rate)s% %(taxname)s": "dont %(rate)s% %(taxname)s",
    "widget\u0004minimum amount to order: %s": "quantit\u00e9 minimum \u00e0 commander: %s",
    "widget\u0004plus %(rate)s% %(taxname)s": "plus %(rate)s% %(taxname)s"
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
    "DATETIME_FORMAT": "j F Y H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%Y",
      "%d.%m.%Y %H:%M:%S",
      "%d.%m.%Y %H:%M:%S.%f",
      "%d.%m.%Y %H:%M",
      "%d.%m.%Y",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j F Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%d.%m.%Y",
      "%d.%m.%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "j N Y H:i",
    "SHORT_DATE_FORMAT": "j N Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
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

