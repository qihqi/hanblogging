<!--
layout: post
title: "Crafting Interpreters Review"
date: 2021-04-25
banner: mountain.png
tags: interpreters
categories: programming
language: zh_CN
-->

今天读完了 Crafing Interpreters 这本书，
感觉还是学到了挺多的东西的。我差不多花了一年的时间，
大约就是每个周末读一章的样子。最后有了一个
完全可以用的编程语言虚拟机实现，感觉还是挺有成就感的。

这本书实现了一个叫Lox的编程语言。这个语言就是作者发明的
教学语言。虽说是个Toy Language，里面的feature也算不少。
variable可以是数字可以是字符串，也可以是object。加减乘除if while都有。
有function, 有class, class有继承和多态，function有closure。感觉比C的feature都多。。但是没有array所以基本不能用。。

Lox 长这样：

```
// 函数有closure
fun returnFunction() {
  var outside = "outside";

  fun inner() {
    print outside;
  }

  return inner;
}

var fn = returnFunction();
fn();

class Breakfast {
  cook() {
    print "Eggs a-fryin'!";
  }

  serve(who) {
    print "Enjoy your breakfast, " + who + ".";
  }
}
// 类可以继承
class Brunch < Breakfast {
  drink() {
    print "How about a Bloody Mary?";
  }
}
```

书中把Lox实现了两边，一边是用Java写的 Tree-walk interpreter。
基本的意思就算把code parse成 Abstract syntax tree (AST) 以后，
就从上到下用recursion解释这个tree。第二边用C写的bytecode vm，就是
现有编译部分把Lox code变成一个基于stack machine的bytecode, 然后有另一个
virtual machine来执行bytecode。stack machine bytecode应该也算是主流了，毕竟
JVM啊，python啊啥的都是用的stack machine。同时还实现了hash table和
garbage collector.

第一部分一开始讲lexing 和 parsing。其实这些部分我一前在
udacity（曾经udacity还是免费的时候）上网课学过了。当时觉得挺枯燥的。
他lexing和parsing都是手磕的，没有用lexer和parser generator。甚至连
正则表达式都没上。但是讲的还挺好懂得一下子就看明白了。感觉后来 parsing 是
个大的research area,所以出了好多牛B的parsing technique，但是其实差别
也没这么大。简单的parser还是现在大多数语言用的。这一章还用到了一个
visitor pattern，好像在GoF的design pattern也有提。这里面更多是为了
get around of Java's type system，我当时复刻用了python就没用visitor pattern.

第二部分比第一部分难不少，我也老实用了C。这样至少看不懂code也可以照抄。
第二部分的compiler是single pass compiler,就是不用把code变成AST，而是之间
生成bytecode.这个设计还听巧妙的，基本逻辑是正常情况下把AST变成bytecode要把树
遍历一边，然而生成这个树也是遍历一边，所以就可以不生成AST之间按照遍历的
顺序写bytecode. 因为C的library是在是啥也没有，上来就手磕了个hash table,然后基于hash table 有了interned string table. 垃圾回收用的是经典的mark and sweep算法。
最后还有一章讲哪些地方可以优化性能。

总体来说感觉干货满满。推荐给大家共同学习。
传送门 -> [https://craftinginterpreters.com/](https://craftinginterpreters.com/)

作者Bob Nystrom是谷歌dart 语言团队的工程师。我记得以前在内网查过感觉6级的样子。
他书的内容应该就是本科第一个编译器课的内容。不过书里面的图和解释啥的
做得真不错,放ppt里面应该能升8🤣🤣🤣
