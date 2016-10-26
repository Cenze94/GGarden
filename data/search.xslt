<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
	xmlns="http://www.w3.org/1999/xhtml"
	xmlns:g="http://www.ggarden.com"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	exclude-result-prefixes="g">
	<xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"
		doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
		doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>
	<xsl:template match="/">
		<html xml:lang="it" lang="it">
			<head>
				<title>Esito ricerca - GGarden</title>
				<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
				<meta name="title" content="GGarden" />
				<meta name="description" content="Azienda specializzata nella vendita di piante e fiori e nel noleggio e vendita di attrezzi e macchine da giardinaggio" />
				<meta name="keywords" content="prodotti, piante, fiori, giardinaggio, attrezzi" />
				<meta name="author" content="Andrea Grendene, Pietro Gabelli, Sebastiano Marchesini, Jacopo Guizzardi" />
				<meta name="language" content="italian it" />
				<meta name="viewport" content="width=device-width" />
				<meta http-equiv="Content-Script-Type" content="application/javascript" />
				<link rel="stylesheet" href="../css/home.css" type="text/css" media="screen and (min-width: 650px)" />
				<link rel="stylesheet" href="../css/print.css" type="text/css" media="print" />
				<link rel="stylesheet" type="text/css" href="../css/small-devices.css" media="screen and (max-width: 650px)" />
				<xsl:comment>
					<![CDATA[[if lte IE 8]><link rel="stylesheet" type="text/css" href="../css/explorer.css"/><![endif]]]>
				</xsl:comment>
				<link rel="icon" href="../img/logo2.png" type="image/png" />
			</head>
			<body>
				<div id="header">
					<h1><span id="logo" xml:lang="en" class="nascosto">GGarden</span></h1>
					<div id="breadcrumbs">
						<span id="rifnav" >Ti trovi in: <a href="../index.html" xml:lang="en">Home</a> / <strong>Esito Ricerca</strong></span>
						<form class="headersearch" action="search.cgi" method="post">
							<fieldset>
								<legend class="nascosto">Cerca un prodotto o un servizio</legend>
								<label for="ricerca" class="nascosto">Inserisci i termini da cercare</label>
								<label for="ricerca" class="nascosto">Cerca un prodotto o un servizio</label>
								<input type="text" name="ricerca" id="ricerca" class="ricerca" accesskey="s" tabindex="1" />
								<input type="submit" name="conferma" id="conferma" class="ricerca" value="Cerca" accesskey="d" tabindex="2"/>
							</fieldset>
						</form>
					</div>
					<div id="contenitore-menu">
						<div class="nascosto">
							<a href="#content" title="salta al contenuto principale">salta direttamente alla lista dei prodotti</a>
						</div>
						<ul class="menu">
							<li><a href="../index.html" id="home" class="nav" xml:lang="en" accesskey="h" tabindex="10">Home </a></li>
							<li><a href="../realizzazioni.html" id="real" class="nav" accesskey="r" tabindex="11">Realizzazioni </a></li>
							<li><a href="checkLog.cgi" id="vend" class="vnav" accesskey="v" tabindex="12">Vendita </a></li>
							<li><a href="../contattaci.html" id="cont" class="nav" accesskey="c" tabindex="13">Contattaci</a></li>
						</ul>
					</div>
				</div>
				<div id="content">
					<xsl:call-template name="esito"/>
				</div>
				<div id="footer" class="footer">
					<div class="footer-left">
						<h3 class="footerlogo"><span id="logo_mini">Ggarden</span></h3>
						<p class="footer-menu">
							<a href="index.html" hreflang="it" xml:lang="en" tabindex="100">Home</a>
							<a href="realizzazioni.html" hreflang="it" tabindex="101">Realizzazioni </a>
							<a href="cgi-bin/checkLog.cgi" hreflang="it" tabindex="102">Vendita</a>
							<a href="contattaci.html" hreflang="it" tabindex="103">Contattaci</a>
						</p>
						<p class="footer-nome-azienda">Ggarden &#169; 2016</p>
					</div>
					<div class="footer-center">
						<div>
							<address class="testo-footer">Via Trieste 63. Padova, Italy</address>
						</div>
						<div>
							<p class="testo-footer"><a href="tel:+1 555 123456">+1 555 123456</a></p>
						</div>
						<div>
							<p xml:lang="en">E-Mail <a href="mailto:ggardengroup@gmail.com" accesskey="e" tabindex="104">ggardengroup@gmail.com</a></p>
						</div>
					</div>
					<div class="footer-right">
						<p class="footer-company-info" title="motto">
							<span class="testo-footer">Gg Garden a servizio</span>
							<span class="testo-footer">L'erba del tuo vicino e&#768; sempre piu&#768; verde. Sii come il tuo vicino,
							chiama G Garden Group</span>
						</p>
					</div>
				</div>
				<script type="text/javascript" src="../script/script.js"></script>
			</body>
		</html>
	</xsl:template>
	<xsl:template name="esito">
		<h2 class="maintitle">ESITO DELLA RICERCA</h2>
		<xsl:for-each select="//g:prodotti/child::*">
			<xsl:if test="name()='p:pianta'">
				<div class="prodotto">
					<h3 class="cnome">
						<xsl:value-of select="g:nome"/>
					</h3>
					<p class="id">
						<xsl:value-of select="@id"/>
					</p>
					<p class="nome_scientifico">
						<xsl:value-of select="g:nome_scientifico"/>
					</p>
					<p class="tipo">
						<xsl:value-of select="g:tipo"/>
					</p>
					<xsl:variable name="nome" select="g:nome"/>
					<xsl:variable name="id" select="@id"/>
					<xsl:variable name="formato" select="@formato"/>
					<xsl:if test="$formato!='no_image'">
						<p class="img"><img src="../img database/{$id}.{$formato}" alt="Foto con {$nome}"/></p>
					</xsl:if>
					<h4>DESCRIZIONE GENERALE</h4>
					<p class="desc">
						<xsl:value-of select="g:descrizione"/>
					</p>
					<xsl:if test="g:dettagli/g:dato">
						<h4>DATI</h4>
						<div class="dati">
							<ul>
								<xsl:for-each select="g:dettagli/g:dato">
									<li>
										<span class="formato">
											<xsl:value-of select="g:nome"/>
											<xsl:if test="g:nome!=''">: </xsl:if>
										</span>
										<span class="contenuto">
											<xsl:value-of select="g:contenuto"/>
										</span>
									</li>
								</xsl:for-each>
							</ul>
						</div>
					</xsl:if>
					<h4>PIANTAGIONE</h4>
					<p class="desc">
						<xsl:value-of select="g:piantagione"/>
					</p>
					<h4>CURA</h4>
					<p class="desc">
						<xsl:value-of select="g:cura"/>
					</p>
					<h4>ALTRE INFORMAZIONI</h4>
					<p class="desc">
						<xsl:value-of select="g:altre_info"/>
					</p>
					<p class="prezzo">
						<xsl:if test="count(g:prezzo/g:pacchetto)&lt;=1">
							<span class="prezzo_singolo">
								&#8364; 
								<xsl:value-of select="g:prezzo/g:pacchetto/g:valore"/>
								<xsl:text> </xsl:text>
								<xsl:value-of select="g:prezzo/g:pacchetto/g:formato"/>
							</span>
						</xsl:if>
						<xsl:if test="count(g:prezzo/g:pacchetto)&gt;1">
							<xsl:for-each select="g:prezzo/g:pacchetto">
								&#8364; 
								<xsl:value-of select="g:valore"/>
								<xsl:text> </xsl:text>
								<xsl:value-of select="g:formato"/>
							</xsl:for-each>
							<hr/>
						</xsl:if>
					</p>
					<div class="nascosto mobile"><a href="#rifnav" title="torna a inizio pagina">Torna direttamente all'inizio della pagina</a></div>
				</div>
			</xsl:if>
			<xsl:if test="name()='p:attrezzo'">
				<div class="prodotto">
					<h3 class="cnome">
						<xsl:value-of select="g:nome"/>
					</h3>
					<p class="id">
						<xsl:value-of select="@id"/>
					</p>
					<p class="tipo">
						<xsl:value-of select="g:tipo"/>
					</p>
					<xsl:variable name="nome" select="g:nome"/>
					<xsl:variable name="id" select="@id"/>
					<xsl:variable name="formato" select="@formato"/>
					<xsl:if test="$formato!='no_image'">
						<p class="img"><img src="../img database/{$id}.{$formato}" alt="Foto con {$nome}"/></p>
					</xsl:if>
					<h4>DESCRIZIONE</h4>
					<p class="desc">
						<xsl:value-of select="g:descrizione"/>
					</p>
					<xsl:if test="g:dettagli/g:dato">
						<h4>DATI</h4>
						<div class="dati">
							<ul>
								<xsl:for-each select="g:dettagli/g:dato">
									<li>
										<span class="formato">
											<xsl:value-of select="g:nome"/>
											<xsl:if test="g:nome!=''">: </xsl:if>
										</span>
										<span class="contenuto">
											<xsl:value-of select="g:contenuto"/>
										</span>
									</li>
								</xsl:for-each>
							</ul>
						</div>
					</xsl:if>
					<p class="prezzo">
						<span class="check">
							&#8364; 
							<xsl:value-of select="g:prezzo/g:pacchetto/g:valore"/>
							<xsl:text> </xsl:text>
							<xsl:value-of select="g:prezzo/g:pacchetto/g:formato"/>
						</span>
					</p>
					<div class="nascosto mobile"><a href="#rifnav" title="torna a inizio pagina">Torna direttamente all'inizio della pagina</a></div>
				</div>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>