package Models;

import java.io.File;

public class Profile {
	String name;

	String avatar;

	String body;
	Rating[] ratings;
	Comment[] comments;
	File[] files;
	Annotation[] annotations;
	Project[] favorites;
	Search[] savedSearches;

	Comment addComment(Comment comment) {
		return comment;
	}

	Rating addRating(Rating rating) {
		return rating;
	}

	Annotation addAnnotation(Annotation annotation) {
		return annotation;
	}

}