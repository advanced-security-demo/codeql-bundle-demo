<aside>
    <table>
        <tr>
            <td><b> Environment: </b> </td>
            <td>
                <form action="index.php" method="get" name="env" >
                    <select name="env" onchange="Refresh(this.value);">
                        <option  value="us_prod">US Production</option>
                        <option  value="us_staging">US Staging</option>
                        <option  value="uk_prod">UK Production</option>
                        <option  'selected' value="uk_staging">UK Staging</option>
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
                    <input type="hidden" name="env" value=<?php echo $env ?> >
                    <input type="text" name="account" />
                    <input type="submit" value="Search">
                </form>
            </td>
        </tr>

        <tr>
            <td> <b> <?php echo "Current Environment: </b></td><td><b>" . $prettyName; ?> </b></td>
        </tr>
    </table>
    <b>Billing Errors:</b>
    <a href="billing.php?env=us_prod&id=1">US</a> | <a href="billing.php?env=uk_prod&id=1">UK</a><br />
    </div> <!-- #main -->
    </div> <!-- #main-container -->
</aside>