package Models;

import java.io.File;
import java.util.Date;

public class Project {
	String name;
	String body;
	boolean isCompleted;
	boolean isActive;
	boolean isModified;
	Category category;

	Date created;
	Date modified;
	Date deadline;

	RegisteredUser[] creator;
	RegisteredUser[] bidders;

	int[] budget;
	Bid[] bids;
	Rating[] ratings;
	Comment[] comments;
	Conversation messages;
	Annotation[] annotations;
	Tag[] tags;
	File[] files;

	public boolean setBudget(int[] range) {
		return isActive;
	}

	public Bid bid(Bid bid) {
		return bid;
	}

	public boolean rate(Rating rating) {
		return isActive;
	}

	public Annotation annotate(Annotation annotation) {
		return annotation;
	}

	public boolean complete() {
		return isActive;
	}

	public boolean acceptBid(Bid bid) {
		return isActive;
	}

}