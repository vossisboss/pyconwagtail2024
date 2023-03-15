# Step Five: Translate your content

Let's work on translating the English content so that we have some content in French to work with as well. We're going to use `wagtail-localize` to help save time by syncing our content from the primary language of our blog.

## Setting up your new locale

To set up a locale for French, go to the lefthand menu, click "Settings", then click "Locales". On the righthand side, click the green "Add a locale" button. In the "Language" dropdown menu, choose "French". 

Beneath the dropdown is an option to synchronize content from the main language of your website. Click the green "Enable" button. Check the "Enabled" checkbox and then select "English" from the "Sync from" menu. Click "Save" to save your changes.

![Screenshot showing how to add a locale to Wagtail](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-03_at_4.21.46_PM.original.png)

Now click "Pages" on the lefthand menu and you'll see there are now _two_ versions of "Badger Blog." One says "English" next to it and the other says "French." Click on the "French" version of "Badger Blog" to edit it. You'll be presented with an option to translate the "Badger Blog" page and all of the pages in the subtree. Check the box to translate all of the pages. 

![Screenshot showing the translate subtree option in Wagtail](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-03_at_4.23.52_PM.original.png)

Now when you open the "Pages" menu, you should see two copies of your page trees: one labeled "English" and another labeled "French".

Click "Edit" for the French version of the "Badger Blog" Page to edit the content. The page will open up in a translation view. The translation view provides the content in the original language and provides you with some different options to translate it.

![Screenshot of the initial translation view for Badger Blog](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-13_at_6.58.01_AM.original.png)

## Translate using PO files

PO files are the file format used by professional translators for translating a variety of structured content, including websites. If you are going to be working with a living, breathing human translator, this could be a good option for your project. The advantages of the PO file is that everything can be translated in one file, and you can send that file to a translator without having to give them access to the admin section of your website.

To use the PO file method, click the "Download PO file" button to download the file. Then either send the file to a translator or use a program like [Poedit](https://poedit.net/download) to edit the file and translate it. Once the file has been translated, you can upload it to your page with the "Upload PO File" button.

Once the file is uploaded, check that there are green checkmarks throughout your page. Click the promote tab too and make sure the slug has been translated as well. Once everything is translated click the big green "Publish in French" button at the bottom to publish the page.

## Translate manually

You can also use the Wagtail Localize plugin to translate content manually as well. This approach is best to use if you decide you are okay with creating a log in for your translator or if someone who will be working on the website regularly is also translating the content. To do manually translation, go through each item on the page and click "Translate". Once you are done adding the translation, click "Save" to save your changes. Do this for each piece of content on the page. Click the "Promote" tab to translate the slug as well. Once you're done, click "Publish in French" at the bottom of the page to publish the page.

**NOTE** Be very careful of using quote marks in your translations. Quote marks in certain languages are different from the quote marks used in HTML. So if there are any links in your content, you need to make sure you're using the right type of quote marks in any HTML included in your translations.

## Machine translation

You can also hit the third button on the page to use the machine translation integration you set up earlier. Now since you set up the Wagtail Localize dummy translator, all it will do here is reverse all of the strings on the page. But it will give you an idea how Deepl or Google Cloud Translation would work if you set them up. If you use this option for your translation, you'll need to click back into the page and publish the results by clicking the "Publish in French" button.

## Translate and publish your pages

Using whichever method you prefer, go through and translate your "Blog" page as well as your "Badgers are brilliant" article. Be sure to publish each one of those pages after you finish adding your translations.

## Syncing content from your main language

Let's try syncing some changes from a blog written in your main language. In the lefthand menu, go to "Pages" then click the arrow to the right until you see "Badgers are brilliant". Play with the language switcher in the admin above it if you want to see how easy it is to switch between the languages. Click on the pencil to open the edit page for "Badgers are brilliant".

![Screenshot of an example of the admin language switcher](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-13_at_7.07.57_AM.original.png)


Scroll down to the body. You're going to add the link to this [YouTube video](https://www.youtube.com/watch?v=c36UNSoJenI) about an escape artist badger to the line "They can break out of zoos." Add the link by highlighting the text and selecting the link option from the menu. When the link menu pops up, click "External link" to add the link to text.

Publish the page with the new changes. After you hit Publish, you'll be returned to the menu for the "Blog" parent page. Hover over "Badgers are brilliant" and click the "More" button. Select "Sync translated pages."

![Screenshot of syncing translated pages](https://www.meagenvoss.com/media/images/Screen_Shot_2022-10-03_at_5.17.00_PM.original.png)

After you set up the sync, navigate to the French version of the page. Your changes to the content will be highlighted in yellow and you can translate them or insert local content. Notice how links and images are separated from the text and can be changed to make them more appealing to a French audience. For example, if you wanted to include a link to a video that was in French or that had French subtitles switched on, you could include a unique link in the French version of the blog. You're welcome to try this by including a link to a different video in the French version. Perhaps this video on [European badgers](https://www.youtube.com/watch?v=PvpNx0Hxtdk) would be more appropriate for your French audience.

All right. Now that we've added some content to your blog and translated it into French, we're going to add a translatable menu and a translatable footer to our website so that you can see how Snippets work in Wagtail as well as how you can translate them.

