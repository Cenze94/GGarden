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
				<title>Esito della ricerca - GGarden</title>
				<meta http-equiv="content-type" content="text/html;charset=utf-8" />
				<meta name="title" content="Esito ricerca - GGarden" />
				<meta name="description" content="Risultato della ricerca all'interno del catalogo dei prodotti di GGarden, comprendente piante ed attrezzi, a Padova" />
				<meta name="keywords" content="ricerca, catalogo, prezzi, esito della ricerca, prodotti, piante, fiori, giardinaggio, attrezzi, Padova" />
				<meta name="author" content="Andrea Grendene, Pietro Gabelli, Sebastiano Marchesini" />
				<meta name="language" content="italian it" />
				<meta name="viewport" content="width=device-width" />
				<link rel="stylesheet" href="../css/home_min.css" type="text/css" media="screen and (min-width: 650px)" />
				<link rel="stylesheet" href="../css/print_min.css" type="text/css" media="print" />
				<link rel="stylesheet" type="text/css" href="../css/small-devices_min.css" media="screen and (max-width: 650px)" />
				<xsl:comment>
					<![CDATA[[if lte IE 8]><link rel="stylesheet" type="text/css" href="../css/explorer_min.css"/><![endif]]]>
				</xsl:comment>
				<link rel="icon" href="../img/logo2.png" type="image/png" />
				<script type="text/javascript" src="../script/script_min.js"></script>
			</head>
			<body>
		        <p class="nascosto">
		            <a title="salta header" href="#contenitore-menu" tabindex="1" accesskey="a">Salta l&apos;intestazione</a>
		        </p>
				<div id="header">
					<h1><span id="logo" xml:lang="en" class="nascosto">GGarden</span></h1>
					<div id="breadcrumbs">
						<span id="rifnav" >Ti trovi in: <a href="../index.html" xml:lang="en">Home</a> / <strong>Esito Ricerca</strong></span>
						<form class="headersearch" action="search.cgi" method="post">
							<fieldset>
		                        <legend class="nascosto">Cerca un prodotto o un servizio</legend>
		                        <label for="ricerca" class="nascosto">Inserisci i termini da cercare</label>
								<input type="text" name="ricerca" id="ricerca" class="ricerca" accesskey="s" tabindex="2" />
                        		<input type="submit" name="conferma" id="conferma" class="ricerca" value="Cerca" accesskey="d" tabindex="3"/>
							</fieldset>
						</form>
					</div>
					<div id="contenitore-menu">
		                <p class="nascosto">
		                    <a href="#content" title="salta al contenuto principale">Salta menu navigazione</a>
		                </p>
						<ul class="menu">
							<li><a href="../index.html" id="home" class="nav" xml:lang="en" accesskey="h" tabindex="10">Home </a></li>
							<li><a href="../realizzazioni.html" id="real" class="nav" accesskey="r" tabindex="11">Realizzazioni</a></li>
							<li><a href="checkLog.cgi" id="vend" class="vnav" accesskey="v" tabindex="12">Vendita </a></li>
							<li><a href="../contattaci.html" id="cont" class="nav" accesskey="c" tabindex="13">Contattaci</a></li>
						</ul>
					</div>
				</div>
				<div id="content">
		            <p class="nascosto">
		                <a title="saltare-contenuto-testuale" href="#footer" tabindex="30" accesskey="b">Salta il contenuto testuale</a>
		            </p>
					<xsl:call-template name="esito"/>
				</div>
				<div id="footer" class="footer">
		            <ul class="nascosto">
		                <li><a href="#header" title="vai-a-inizio-pagina" tabindex="100" accesskey="i">Torna all&apos;inizio pagina</a></li>
		                <li><a href="#finePagina" title="vai-a-fine-pagina" tabindex="110" accesskey="f">Vai a fine pagina</a></li>
		            </ul>
					<div class="footer-left">
						<h3 class="footerlogo"><span id="logo_mini">Ggarden</span></h3>
						<p class="footer-menu, testo-footer">
							<a href="../index.html" hreflang="it" xml:lang="en" tabindex="100">Home</a> | 
							<a href="../realizzazioni.html" hreflang="it" tabindex="101">Realizzazioni</a> | 
							<a href="checkLog.cgi" hreflang="it" tabindex="102">Vendita</a> | 
							<a href="../contattaci.html" hreflang="it" tabindex="103">Contattaci</a>
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
						<div class="testo-footer, center">
                            <p>
                                <a href="http://validator.w3.org/check?uri=referer"><img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a>
                                <a href="http://jigsaw.w3.org/css-validator/check/referer"><img style="border:0;width:88px;height:31px" src="http://jigsaw.w3.org/css-validator/images/vcss" alt="Valid CSS!" /></a>
                            </p>
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
        		<p id="finePagina"></p>
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
	                                <li class="info">
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
						<xsl:for-each select="g:prezzo/g:pacchetto">
							<span class="check">
								&#8364; 
								<xsl:value-of select="g:valore"/>
								<xsl:text> </xsl:text>
								<xsl:value-of select="g:formato"/>
							</span>
						</xsl:for-each>
					</p>
					<hr/>
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
                                <li class="info">
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
						<xsl:for-each select="g:prezzo/g:pacchetto">
							<span class="check">
								&#8364; 
								<xsl:value-of select="g:valore"/>
								<xsl:text> </xsl:text>
								<xsl:value-of select="g:formato"/>
							</span>
						</xsl:for-each>
					</p>
					<hr/>
					<div class="nascosto mobile"><a href="#rifnav" title="torna a inizio pagina">Torna direttamente all'inizio della pagina</a></div>
				</div>
			</xsl:if>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>