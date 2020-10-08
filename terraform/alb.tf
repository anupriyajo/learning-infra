resource "aws_alb" "python-alb" {
  name            = "python-alb"
  subnets         = aws_subnet.public.*.id
  security_groups = [aws_security_group.python-alb-sg.id]
}
