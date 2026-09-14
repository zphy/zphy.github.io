# Graduate Student Profiles

## Scope

Add Nathan Constantinides, Shaun Pexton, and Xicheng (Tristan) Wang to the existing “Current Team” section of the People page. Preserve the page’s current jemdoc card structure and styling.

## Content

Each profile will contain the student’s full name, the title “PhD Student,” and the following supplied biography. Markdown emphasis and escaped blank-line markers from the request are input formatting, not page content.

Nathan Constantinides:

> Nathan is a physics PhD student in quantum information theory. Prior to MIT, he obtained dual bachelor's degrees in physics and computer science from the University of Maryland, College Park, advised by Professors Gorshkov and Childs. Nathan is interested in the intersection of quantum error correction, compilation, and quantum simulation algorithms.

Shaun Pexton, as two paragraphs:

> Shaun grew up in Hong Kong, Singapore, and the UK. He received his B.S. in Applied Physics and Computer Science from Yale University, where he was awarded the Josiah Willard Gibbs Prize and the Applied Physics Prize.
>
> His research spans quantum error correction, fault-tolerant architectures, and device physics. At Yale he worked with Aleksander Kubica and Yongshan Ding, and held research positions at Quantum Motion in Oxford and ASML in Wilton. He is particularly interested in questions at the interface of theory and experiment in quantum computing.

Xicheng (Tristan) Wang, as two paragraphs:

> Tristan grew up in Jiangsu, China. He obtained a B.S. in Mathematics and Physics from Tsinghua University in Beijing, and he is currently a graduate student in the MIT Department of Physics.
>
> His research lies at the intersection of quantum many-body physics and quantum information, with an emphasis on how ideas from the two fields inspire one another. He is also interested in concrete architectures for quantum computers and collaborations with experimental groups. Outside of research, he enjoys sports, movies, and traveling.

The profiles will appear after Kaavya Sahay and before Kuro in the order Nathan, Shaun, and Tristan, following the order in which the profiles were supplied.

## Images

Copy `/Users/hyzhou/Downloads/Nathan Constantinides - NSF- F-1-cropped.jpg` to `data/nathan_constantinides.jpg`. Create `data/shaun_pexton.jpg` as a square crop of `/Users/hyzhou/Downloads/2U1A6819-CHOSEN.JPG`. Center Shaun in the crop with his full head and upper torso visible. Copy `/Users/hyzhou/Downloads/王希呈社媒图片.jpg` to `data/xicheng_tristan_wang.jpg` without cropping. Do not modify the source files in Downloads. All three page entries will use the existing 210-pixel image width.

## Generation and Verification

Edit the canonical `people.jemdoc` source and regenerate `people.html` with `./jemdoc -c mysite.conf people.jemdoc`. Verify that all three generated cards contain the correct names, titles, biographies, image paths, ordering, and balanced HTML structure. Check all three image files and inspect the rendered page visually. Run `git diff --check` and preserve unrelated working-tree files.
