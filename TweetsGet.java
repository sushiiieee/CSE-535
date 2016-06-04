package twitter_package;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.LinkedList;

import org.json.simple.JSONValue;

import twitter4j.FilterQuery;
import twitter4j.HashtagEntity;
import twitter4j.JSONArray;
import twitter4j.StallWarning;
import twitter4j.Status;
import twitter4j.StatusDeletionNotice;
import twitter4j.StatusListener;
import twitter4j.TwitterStream;
import twitter4j.TwitterStreamFactory;
import twitter4j.URLEntity;
import twitter4j.User;
import twitter4j.conf.ConfigurationBuilder;
import org.json.simple.JSONObject;


public class TwitterStreamCosumer {
    public static void main(String[] args) throws IOException {
    	
    	
        ConfigurationBuilder cb = new ConfigurationBuilder();
        cb.setDebugEnabled(true);

        cb.setOAuthConsumerKey("key");
		cb.setOAuthConsumerSecret("secret");
		cb.setOAuthAccessToken("token");
		cb.setOAuthAccessTokenSecret("tokenSecret");

        TwitterStream twitterStream = new TwitterStreamFactory(cb.build()).getInstance();
        
        String fileName = "tweets.json";
		final PrintWriter p=new PrintWriter (new FileWriter(fileName,true));
       
        final JSONArray jsonArray = new JSONArray();
        
        StatusListener listener = new StatusListener() {
        	
        	
        	
        	//FileWriter fileWriter = null ;
			
			
        	
        	int count=0;

            @Override
            public void onException(Exception arg0) {
                // TODO Auto-generated method stub

            }

            @Override
            public void onDeletionNotice(StatusDeletionNotice arg0) {
                // TODO Auto-generated method stub

            }

            @Override
            public void onScrubGeo(long arg0, long arg1) {
                // TODO Auto-generated method stub

            }

            @Override
            public void onStatus(Status status) {
            	
            	
				
        		try {
        			
        			
        			boolean flag=true;
        			
//        			if(count==0){
//        				p 
//        			}
        			
        			//System.out.println("CSV file was created successfully !!!");
        			 User user = status.getUser();
                     
                     
                     String username = status.getUser().getScreenName();
                     //System.out.println(status.getCreatedAt());
                     String profileLocation = user.getLocation();
                     //System.out.println(profileLocation);
                     long tweetId = status.getId(); 
                     //System.out.println(tweetId);
                     String content = status.getText();
                     
                     //System.out.println(content);
                     LinkedList list = new LinkedList();
                     
                    
                     LinkedList expand = new LinkedList();
                     if(status.getURLEntities().length>0){
                    	 
                    	 for(URLEntity i : status.getURLEntities()){
                    		 expand.add(i.getExpandedURL());
                    	 }
                    	 String jsonexpand = JSONValue.toJSONString(expand);
                         //System.out.println(jsonexpand);
                    	 //System.out.println(status.getURLEntities()[0].getExpandedURL());
                     }
                     LinkedList hashtag = new LinkedList();
                     if(status.getHashtagEntities().length>0){
                    	 for(HashtagEntity i : status.getHashtagEntities()){
                     hashtag.add(i.getText());
                     }
                    	 String jsonhash = JSONValue.toJSONString(hashtag);
                         //System.out.println(jsonhash);
                     }

                     JSONObject obj=new JSONObject();
                     obj.put("id",String.valueOf(status.getId()));
                     obj.put("lang",status.getLang());
                     String lang=status.getLang().toString();
                     String text="";
                     if(lang.equals("en")){
                    	text=text.concat("text_en");
                     }
                     else if(lang.equals("de")){
                		 text=text.concat("text_de");
                     }
                     else if(lang.equals("ru")){
                		 text=text.concat("text_ru");
                     }
                     else if(lang.equals("fr")){
                		 text=text.concat("text_fr");
                     }
                     else if(lang.equals("ar")){
                		 text=text.concat("text_ar");
                     }
                     else if(lang.equals("es")){
                		 text=text.concat("text_es");
                     }
                     
                     obj.put(text,status.getText());       //change the name of this field depending on the language
                     
                     SimpleDateFormat ft = new SimpleDateFormat ("yyyy-MM-dd'T'HH:mm:ss.SSS'Z'");
                     obj.put("created_at",ft.format(status.getCreatedAt()));
                     obj.put("tweet_hashtags",hashtag);
                     obj.put("expanded_urls",expand);
                     obj.put("user_screen_name" , status.getUser().getScreenName());
                     obj.put("location",status.getUser().getLocation());
                     obj.put("retweet_status", status.isRetweet());
                     if (status.getQuotedStatus() == null)
							flag = false;

                     obj.put("quote_status", flag);
                     obj.put("favorite_count", status.getFavoriteCount());
                     obj.put("retweet_count", status.getRetweetCount());
                     obj.put("favorited_status", status.isFavorited());
                     obj.put("user_id", status.getUser().getId());
                     obj.put("user_verified", status.getUser().isVerified());
                     obj.put("user_followers_count", status.getUser().getFollowersCount());
                     obj.put("user_name", status.getUser().getName());
                     String jsonText = JSONValue.toJSONString(obj);
                     jsonArray.put(obj);
                     String jsonstring =jsonText.toString();
                     //System.out.println(status);
                     //System.out.println(obj);
                     //System.out.println(jsonText);
                     //System.out.println(jsonstring);
                     //p.append(status +"\n\n");
                     p.append(jsonstring);
                     count++;
                     //System.out.println(count);
                     //p.close();
                     p.append(",");
                     if(count==500){
                    	 //p.append(jsonArray.toString());
                    	 p.close();
                    	 //System.out.println("CSV file was created successfully !!!");
                         System.exit(0);
                 		}
                    
                      	
        			
        		} catch (Exception e) {
        			System.out.println("Error in CsvFileWriter !!!");
        			e.printStackTrace();
        		} 
        			
        		//System.out.println("\n\n");
        		

            }

            @Override
            public void onTrackLimitationNotice(int arg0) {
                // TODO Auto-generated method stuba

            }

			@Override
			public void onStallWarning(StallWarning arg0) {
				// TODO Auto-generated method stub
				
			}

        };
        FilterQuery fq = new FilterQuery();
    
        String keywords_en[] = {"Technology","Cloud Computing","CPU","Cybersecurity","Cybercrime","Download","Firewall", "scientific discoveries","Internet","Java","Megabyte","Network","operating system","Processor","Router","Server","Troubleshooting","Website"};
        String keywords_ru[] = {"??????????", "??????????", "?????????????", "???????????", "??????? ??????????", "???????????????", "?????????????", "???????? ?????", "?????????????", "?????????", "?????"};
        String keywords_de[] = {"Technologie", "Ingenieurwesen", "Biotechnologie", "Informationen", "High-Tech-Technologie", "Automatisierung", "digitales Kommunikation", "Robotik", "Computer", "Techno", "Telekommunikation" , "gut", "Ingenieur", "Cloud Computing", "CPU", "Informationssicherheit", "Cyberkriminalität", "Datenbank", "Download", "Verschlüsselung", "Firewall", "Java", "Netzwerk","Betriebssystem","Bericht","Router","Server","Fehlersuche","Ort","Suchmaschinen","wissenschaftliche Wissenschaft"};
        String keywords_ar[]={};
        String keywords_fr[]={};
        String keywords_es[]={};
        
        String language="en";  //change the language here
        
        if(language.equals("en")){
        	fq.track(keywords_en);  
        	fq.language("en");
        }
        else if(language.equals("de")){
        	fq.track(keywords_de);  
        	fq.language("de");
        }
        else if(language.equals("ru")){
        	fq.track(keywords_ru);  
        	fq.language("ru");
        }
        else if(language.equals("ar")){
        	fq.track(keywords_ar);  
        	fq.language("ar");
        }
        else if(language.equals("es")){
        	fq.track(keywords_es);  
         	fq.language("es");
        }
        else if(language.equals("fr")){
        	fq.track(keywords_fr);  
        	fq.language("fr");
        }
        twitterStream.addListener(listener);
        twitterStream.filter(fq);  

    }
}
