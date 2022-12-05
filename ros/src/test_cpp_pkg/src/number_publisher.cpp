#include "example_interfaces/msg/string.hpp"
#include "rclcpp/rclcpp.hpp"

class number_publisher : public rclcpp::Node  // MODIFY NAME
{
   public:
    number_publisher() : Node("number_publisher"), name_("Björn")  // MODIFY NAME
    {
        publisher_ = this->create_publisher<example_interfaces::msg::String>("number_publisher", 10);
        timer_ = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&number_publisher::publish, this));
        number_ = rand() % 100 + 1;

        RCLCPP_INFO(this->get_logger(), "cpp number_publisher has been started...");
    }

   private:
    void publish() {
        auto msg = example_interfaces::msg::String();
        number_ = rand() % 100 + 1;
        msg.data = std::string(std::to_string(number_));
        publisher_->publish(msg);
    }

    int number_;
    std::string name_;
    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<number_publisher>();  // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}