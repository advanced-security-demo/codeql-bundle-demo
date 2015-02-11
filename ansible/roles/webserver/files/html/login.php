<?php
require_once("top.php");

if ($_GET['error'] == '1') {
    print '<div style="color:red;">';
    print 'You must be logged in to do that.';
    print '</div>';
}
?>
    <div id="main-container">
        <div id="main" class="wrapper clearfix">
            <content>
                <form style="margin-left:20px;" class="form-horizontal" method="POST" action="auth.php">
                    <div class="control-group">
                        <div class="controls">
                            <input type="text" id="user" name="user" placeholder="demo">
                        </div>
                    </div>
                    <div class="control-group">
                        <div class="controls">
                            <input type="password" id="pass" name="pass" placeholder="demo">
                        </div>
                    </div>
                    <div class="control-group">
                        <div class="controls">
                            <label class="checkbox">
                                <input type="checkbox"> Remember me
                            </label>
                            <button type="submit" class="btn">Sign in</button>
                        </div>
                    </div>
                </form>
            </content>
<?php
#require_once("left.php");
require_once("footer.php");
?>