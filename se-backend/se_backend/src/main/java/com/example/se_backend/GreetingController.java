package com.example.se_backend;

import java.util.concurrent.atomic.AtomicLong;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import jdbm.RecordManager;
import jdbm.RecordManagerFactory;
import jdbm.htree.HTree;
import jdbm.helper.FastIterator;

@RestController
public class GreetingController {

	private static final String template = "Hello, %s!";
	private final AtomicLong counter = new AtomicLong();

	@GetMapping("/greeting")
	public Greeting greeting(@RequestParam(value = "name", defaultValue = "World") String name) {
		return new Greeting(counter.incrementAndGet(), String.format(template, name));
	}

    @GetMapping("/test")
	public TestType testJDBM(@RequestParam(value = "key", defaultValue = "key1") String key) {
		try
		{
			RecordManager recman;
			HTree hashtable;
			recman = RecordManagerFactory.createRecordManager("testRM");
			long recid = recman.getNamedObject("ht1");
			if (recid != 0)
			{
				hashtable = HTree.load(recman, recid);		
			}
			else
			{
				hashtable = HTree.createInstance(recman);
				recman.setNamedObject( "ht1", hashtable.getRecid() );
			}
		
			// hashtable.put("key1", "context 1");
			// hashtable.put("key2", "context 2");
			// hashtable.put("key3", "context 3");
            // hashtable.put("key4", "context 4");
		
			String content = hashtable.get(key).toString();
		
			// hashtable.remove( "key2" );
        
			// FastIterator iter = hashtable.keys();
			// String key;	
			// while( (key = (String)iter.next())!=null)
			// {
			// 	System.out.println(key + " : " + hashtable.get(key));
			// }
	
			recman.commit();
			
			recman.close();
            return new TestType(key, content);
		}
		catch(java.io.IOException ex)
		{
			System.err.println(ex.toString());
            return new TestType(key, "not find");
		}
	}
}