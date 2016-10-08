<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:g="http://www.ggarden.com"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    exclude-result-prefixes="g">
    <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/>
    <xsl:template match="/">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="it" lang="it">
            <head>
                <title>Lista Prodotti - GGarden</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                <meta name="title" content="GGarden" />
                <meta name="description" content="Azienda specializzata nella vendita di piante e fiori e nel noleggio e vendita di attrezzi e macchine da giardinaggio" />
                <meta name="keywords" content="prodotti, piante, fiori, giardinaggio, attrezzi" />
                <meta name="author" content="Andrea Grendene, Pietro Gabelli, Sebastiano Marchesini, Jacopo Guizzardi" />
                <meta name="language" content="italian it" />
                <link rel="stylesheet" href="../css/home.css" type="text/css" media="screen" />
                <link rel="stylesheet" href="../css/print.css" type="text/css" media="print" />
                <link rel="stylesheet" type="text/css" href="../css/small-devices.css" media="screen and (max-width: 650px)" />
            </head>
            
            <body onload="caricamentoPannelloAdmin();">
                <div id="header">
                    <h1><span id="logo" xml:lang="en" class="nascosto">GGarden</span></h1>
                    <div id="contenitore-login">
                        <input id="button_admin" type="button" onclick="nascondi();" value="Accedi come amministratore"/>
                        <div id="login">
                            <form action="log.cgi" method="get">
                                <fieldset>
                                    <legend>Login amministratore</legend>
                                    <div class="modal hide fade in">
                                        <div class="control-group">
                                            <label for="inputUsername">Username:</label>
                                            <input type="text" name="inputUsername" id="inputUsername" tabindex="-1"/>
                                        </div>
                                        <div class="control-group">
                                            <label for="inputPassword">Password :</label>
                                            <input type="password" name="inputPassword" id="inputPassword" tabindex="-2" />
                                        </div>
                                        <input type="hidden" name="update" value="no"/>
                                        <button type="submit" id="accedi">Accedi</button>
                                    </div>
                                </fieldset>
                            </form>
                        </div>
                    </div>
                </div>
                <div id="breadcrumbs">
                    <form class="headersearch" action="search.cgi" method="get">
                        <fieldset>
                            <span id="rifnav" >Ti trovi in: <a href="../home.html" xml:lang="en" accesskey="h">Home</a> / <b>Prodotti</b></span>
                            <label for="ricerca" class="nascosto">Cerca un prodotto o un servizio</label>
                            <input type="text" name="ricerca" id="ricerca" class="ricerca" accesskey="s" tabindex="1" />
                            <input type="submit" name="conferma" id="conferma" class="ricerca" value="Cerca" accesskey="c" tabindex="2"/>
                        </fieldset>
                    </form>
                </div>
                
                
                <div id="contenitore-menu">
                    <div class="nascosto">
                        <a href="#content" title="salta al contenuto principale">salta direttamente alla lista dei prodotti</a>
                    </div>
                    <ul class="menu">
                        <li><a href="../home.html" id="home" class="nav" xml:lang="en" accesskey="h" tabindex="10">Home </a></li>
                        <li><a href="../realizzazioni.html" id="real" class="nav" accesskey="r" tabindex="11">Realizzazioni </a></li>
                        <li><a href="checkLog.cgi" id="vend" class="vnav" accesskey="v" tabindex="12">Vendita </a></li>
                        <li><a href="../contattaci.html" id="cont" class="nav" accesskey="c" tabindex="13">Contattaci</a></li>

                    </ul>
                </div>
                
                
                
                
                <div id="content">
                    
                    <div id="piante">
                        <xsl:call-template name="piante"/>
                    </div>
                    <div id="attrezzi">
                        <xsl:call-template name="attrezzi"/>
                    </div>
                </div>
                
                <div id="footer" class="footer">
                    <div class="footer-left">
                        <h3 class="footerlogo"><span id="logo_mini">Ggarden</span></h3>
                        <p class="footer-menu">
                            <a href="../home.html" hreflang="it" xml:lang="en" accesskey="h" tabindex="100">Home</a>
                            
                            <a href="../realizzazioni.html" hreflang="it" accesskey="r" tabindex="101">Realizzazioni </a>
                            
                            <a href="checkLog.cgi" hreflang="it" accesskey="v" tabindex="102">Vendita</a>
                            
                            <a href="../contattaci.html" hreflang="it" accesskey="c" tabindex="103">Contattaci</a>
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
    
    
    <xsl:template name="piante">
        <p id="titoloPiante"><h2 class="maintitle">PIANTE</h2></p>
        <xsl:for-each select="g:prodotti/g:pianta">
            <xsl:sort select="g:nome"/>
            <div class="prodotto">
                <form action="" method="post">
                    <h3 class="cnome"><xsl:value-of select="g:nome"/></h3>
                    <p class="id"><xsl:value-of select="@id"/></p>
                    <p class="nome_scientifico"><xsl:value-of select="g:nome_scientifico"/></p>
                    <p class="tipo"><xsl:value-of select="g:tipo"/></p>
                    <xsl:variable name="nome" select="g:nome"/>
                    <xsl:variable name="id" select="@id"/>
                    <xsl:variable name="formato" select="@formato"/>
                    <xsl:if test="$formato!='no_image'">
                        <p class="img"><img src="../img database/{$id}.{$formato}" alt="Foto con {$nome}"/></p>
                    </xsl:if>
                    <h4>DESCRIZIONE GENERALE</h4>
                    <p class="desc"><xsl:value-of select="g:descrizione"/></p>
                    <xsl:if test="g:dettagli/g:dato">
                        <h4>DATI</h4>
                        <p class="dati"><ul>
                            <xsl:for-each select="g:dettagli/g:dato">
                                <li class="info"><span class="formato"><xsl:value-of select="g:nome"/><xsl:if test="g:nome!=''">: </xsl:if></span><span class="contenuto"><xsl:value-of select="g:contenuto"/></span></li>
                            </xsl:for-each>
                        </ul></p>
                    </xsl:if>
                    <h4>PIANTAGIONE</h4>
                    <p class="desc"><xsl:value-of select="g:piantagione"/></p>
                    <h4>CURA</h4>
                    <p class="desc"><xsl:value-of select="g:cura"/></p>
                    <h4>ALTRE INFORMAZIONI</h4>
                    <p class="desc"><xsl:value-of select="g:altre_info"/></p>
                    <fieldset class="riquadro_prezzi">
                        <p class="prezzo">
                            <xsl:if test="count(g:prezzo/g:pacchetto)&lt;=1">
                                <span class="prezzo_singolo">&#8364; <xsl:value-of select="g:prezzo/g:pacchetto/g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:prezzo/g:pacchetto/g:formato"/></span>
                            </xsl:if>
                            <xsl:if test="count(g:prezzo/g:pacchetto)&gt;1">
                                <xsl:for-each select="g:prezzo/g:pacchetto">
                                    <span class="check"><xsl:variable name="num_prezzo" select="position()"/>
                                        <xsl:if test="$num_prezzo=1"> &#8364; <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></xsl:if>
                                        <xsl:if test="$num_prezzo&gt;1"> &#8364; <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></xsl:if>
                                    </span>
                                </xsl:for-each>
                            </xsl:if>
                        </p>
                    </fieldset>
                </form>
            </div><hr/>
        </xsl:for-each>
    </xsl:template>
    <xsl:template name="attrezzi">
        <p id="titoloAttrezzi"><h2 class="maintitle">ATTREZZI E MACCHINARI</h2></p>
        <xsl:for-each select="g:prodotti/g:attrezzo">
            <xsl:sort select="g:nome"/>
            <div class="prodotto">
                <form action="" method="post">
                    <h3 class="cnome"><xsl:value-of select="g:nome"/></h3>	
                    <p class="id"><xsl:value-of select="@id"/></p>
                    <p class="tipo"><xsl:value-of select="g:tipo"/></p>
                    <xsl:variable name="nome" select="g:nome"/>
                    <xsl:variable name="id" select="@id"/>
                    <xsl:variable name="formato" select="@formato"/>
                    <xsl:if test="$formato!='no_image'">
                        <p class="img"><img src="../img database/{$id}.{$formato}" alt="Foto con {$nome}"/></p>
                    </xsl:if>
                    <h4>DESCRIZIONE</h4>
                    <p class="desc"><xsl:value-of select="g:descrizione"/></p>
                    <xsl:if test="g:dettagli/g:dato">
                        <h4>DATI</h4>
                        <p class="dati"><ul>
                            <xsl:for-each select="g:dettagli/g:dato">
                                <li class="info"><span class="formato"><xsl:value-of select="g:nome"/><xsl:if test="g:nome!=''">: </xsl:if></span><span class="contenuto"><xsl:value-of select="g:contenuto"/></span></li>
                            </xsl:for-each>
                        </ul></p>
                    </xsl:if>
                    <fieldset class="riquadro_prezzi">
                        <p class="prezzo">
                            <xsl:if test="count(g:prezzo/g:pacchetto)&lt;=1">
                                <span class="prezzo_singolo">&#8364; <xsl:value-of select="g:prezzo/g:pacchetto/g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:prezzo/g:pacchetto/g:formato"/></span>
                            </xsl:if>
                            <xsl:if test="count(g:prezzo/g:pacchetto)&gt;1">
                                <xsl:for-each select="g:prezzo/g:pacchetto">
                                    <span class="check"><xsl:variable name="num_prezzo" select="position()"/>
                                        <xsl:if test="$num_prezzo=1"> &#8364; <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></xsl:if>
                                        <xsl:if test="$num_prezzo&gt;1"> &#8364; <xsl:value-of select="g:valore"/><xsl:text> </xsl:text><xsl:value-of select="g:formato"/></xsl:if>
                                    </span>
                                </xsl:for-each>
                            </xsl:if>
                        </p>
                    </fieldset>
                </form>
            </div>	<hr/>
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>
