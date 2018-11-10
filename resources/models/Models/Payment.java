package Models;

import java.io.File;
import java.util.Date;

public class Payment {
	Date created;
	RegisteredUser user;
	RegisteredUser recipient;
	boolean isWithdrawn;
	boolean isCompleted;
	File[] report;

}