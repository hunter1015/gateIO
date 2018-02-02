import numpy.random as random
 
random.seed(42)
 
# 做10000次实验
n_tests = 10000
 
# 生成每次实验的奖品所在的门的编号
# 0表示第一扇门，1表示第二扇门，2表示第三扇门
winning_doors = random.randint(0, 3, n_tests)
 
# 记录如果换门的中奖次数
change_mind_wins = 0
 
# 记录如果坚持的中奖次数
insist_wins = 0
 
# winning_door就是获胜门的编号
for winning_door in winning_doors:
 
    # 随机挑了一扇门
    first_try = random.randint(0, 3)
    
    # 其他门的编号
    remaining_choices = [i for i in range(3) if i != first_try]
  
    # 没有奖品的门的编号，这个信息只有主持人知道
    wrong_choices = [i for i in range(3) if i != winning_door]
 
    # 一开始选择的门主持人没法打开，所以从主持人可以打开的门中剔除
    if first_try in wrong_choices:
        wrong_choices.remove(first_try)
    
    # 这时wrong_choices变量就是主持人可以打开的门的编号
    # 注意此时如果一开始选择正确，则可以打开的门是两扇，主持人随便开一扇门
    # 如果一开始选到了空门，则主持人只能打开剩下一扇空门
    screened_out = random.choice(wrong_choices)
    remaining_choices.remove(screened_out)
    
    # 所以虽然代码写了好些行，如果策略固定的话，
    # 改变主意的获胜概率就是一开始选错的概率，是2/3
    # 而坚持选择的获胜概率就是一开始就选对的概率，是1/3
    
    # 现在除了一开始选择的编号，和主持人帮助剔除的错误编号，只剩下一扇门
    # 如果要改变注意则这扇门就是最终的选择
    changed_mind_try = remaining_choices[0]
 
    # 结果揭晓，记录下来
    change_mind_wins += 1 if changed_mind_try == winning_door else 0
    insist_wins += 1 if first_try == winning_door else 0
 
# 输出10000次测试的最终结果，和推导的结果差不多：
# You win 6616 out of 10000 tests if you changed your mind
# You win 3384 out of 10000 tests if you insist on the initial choice
print(
    'You win {1} out of {0} tests if you changed your mind\n'
    'You win {2} out of {0} tests if you insist on the initial choice'.format(
        n_tests, change_mind_wins, insist_wins
        )
)