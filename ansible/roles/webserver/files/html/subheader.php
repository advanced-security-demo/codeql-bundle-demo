<aside>
    <table>
        <tr>
            <td><b> Environment: </b> </td>
            <td>
                <form action="index.php" method="get" name="env" >
                    <select name="env" onchange="Refresh(this.value);">
                        <option <?php if ($env == 'us_prod') print 'selected'; ?> value="us_prod">US Production</option>
                        <option <?php if ($env == 'us_staging') print 'selected'; ?> value="us_staging">US Staging</option>
                        <option <?php if ($env == 'uk_prod') print 'selected'; ?> value="uk_prod">UK Production</option>
                        <option <?php if ($env == 'uk_staging') print 'selected'; ?> value="uk_staging">UK Staging</option>
                    </select>
                </form>
            </td>
        </tr>
        <tr>
            <td>
                <b>Account Number: </b>
            </td>
            <td>
                <form action="account.php" method="get">
                    <input type="hidden" name="env" value=<? echo $env ?> >
                    <input type="text" name="account" />
                    <input type="submit" value="Search">
                </form>
            </td>
        </tr>
        <tr>
            <td>
                <b>Server IP:</b>
            </td>
            <td>
                <form action="serverDetail.php" method="get">
                    <input type="hidden" name="env" value=<? echo $env ?> >
                    <input type="text" name="serverIp" />
                    <input type="submit" value="Search">
                </form>
            </td>
        </tr>
        <tr>
            <td>
                <b>Transaction Search:</b>
            </td>
            <td>
                <form action="transaction.php" method="get">
                    <input type="hidden" name="env" value=<? echo $env ?> >
                    <input type="text" name="trackingId" size=40>
                    <input type="submit" value="Search">
                </form>
            </td>
        </tr>
        <tr>
            <td> <b> <? echo "Current Environment: </b></td><td><b>" . $prettyName; ?> </b></td>
        </tr>
    </table>
    <b>Signup Errors:</b>
    <a href="signupErrors.php?env=us_prod">US</a> | <a href="signupErrors.php?env=uk_prod">UK</a><br />
    <b>Billing Errors:</b>
    <a href="billing.php?env=us_prod">US</a> | <a href="billing.php?env=uk_prod">UK</a><br />
    <b>BillingV2 Errors:</b>
    <a href="billing2.php?env=us_prod">US</a> | <a href="billing2.php?env=uk_prod">UK</a><br />
    <b>Sites Errors:</b>
    <a href="sites.php?env=us_prod">US</a> | <a href="sites.php?env=uk_prod">UK</a><br />
    <b>GetPDFInvoice Errors:</b>
    <a href="GetPDFInvoice.php?env=us_prod">US</a> | <a href="GetPDFInvoice.php?env=uk_prod">UK</a>
    </div> <!-- #main -->
    </div> <!-- #main-container -->
</aside>